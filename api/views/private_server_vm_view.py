from django.db import transaction
from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.filters import filter_private_server_vm
from api.helpers import Paginator, sort_queryset, get_model_fields
from api.helpers import get_valid_ip
from api.helpers.cloudflare import delete_cloudflare_dns
from api.helpers.exceptions import AnsibleError
from api.models import PrivateServerVM, ServerType, PrivateServer, AppUser
from api.permissions import IsPrivateUser
from api.serializers import PrivateServerVMSerializer, ObjectIdSerializer, PrivateServerVmQueryParamsSerializer, \
    PrivateServerVMDeploySerializer
from api.tasks import handle_hardening, handle_proxmox_deploy, handle_proxmox_stop, handle_proxmox_start, \
    handle_vm_destroy
from api.utils.crypto import decrypt, encrypt


@extend_schema(
    responses={200: PrivateServerVMSerializer},
    request=PrivateServerVMSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_private_server_vm(request):
    pk = request.data.pop('id', None)

    if pk is None or pk == '':
        serializer = PrivateServerVMSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        obj = get_object_or_404(PrivateServerVM, id=pk)
        serializer = PrivateServerVMSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: PrivateServerVMSerializer(many=True)},
    request=PrivateServerVmQueryParamsSerializer
)
@api_view(['POST'])
@permission_classes([IsPrivateUser])
def get_private_server_vms(request):
    queryset = PrivateServerVM.objects.all()

    query_params = PrivateServerVmQueryParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    queryset = filter_private_server_vm(queryset, query_params.data)
    fields = get_model_fields(PrivateServerVM)
    queryset = sort_queryset(queryset, query_params.data, fields, 'name')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = PrivateServerVMSerializer(queryset, many=True)
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    responses={200: PrivateServerVMSerializer},
    request=ObjectIdSerializer
)
@api_view(['POST'])
def get_private_server_vm_by_id(request):
    instance = get_object_or_404(PrivateServerVM, id=request.data.get('id'))
    serializer = PrivateServerVMSerializer(instance)
    return Response(serializer.data)


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
@transaction.atomic()
def delete_private_server_vm(request):
    obj: PrivateServerVM = get_object_or_404(PrivateServerVM, id=request.data.get('id'))
    if obj.vm_id is not None:
        task = handle_vm_destroy.delay(obj.id)
        return Response(f'{task.id}')
    else:
        obj.delete()
        return Response('vm did not have vm_id so row was deleted from db')


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def start_private_server_vm(request):
    obj: PrivateServerVM = get_object_or_404(PrivateServerVM, id=request.data.get('id'))
    task = handle_proxmox_start.delay(obj.id)
    return Response(f'{task.id}')


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def stop_private_server_vm(request):
    obj: PrivateServerVM = get_object_or_404(PrivateServerVM, id=request.data.get('id'))
    task = handle_proxmox_stop.delay(obj.id)
    return Response(f'{task.id}')


@extend_schema(
    request=ObjectIdSerializer,
    responses=PrivateServerVMSerializer,
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def harden_private_server_vm(request):
    server_vm = get_object_or_404(PrivateServerVM, id=request.data.get('id'))

    task = handle_hardening.delay(
        server_vm.id,
        ServerType.PRIVATE_VM,
        host=server_vm.ip,
        username=server_vm.username,
        password=server_vm.password
    )
    return Response(f'{task.id}')


@extend_schema(
    request=PrivateServerVMDeploySerializer,
    responses=PrivateServerVMSerializer,
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def deploy_private_server_vm(request):
    # return Response(request.data.get('vm_name'))
    if PrivateServerVM.objects.filter(
            vm_name__iexact=str(request.data.get('vm_name')),
            private_server=request.data.get('private_server_id')
    ).exists():
        return Response('another vm with this name already exists', status=status.HTTP_400_BAD_REQUEST)

    private_server = get_object_or_404(PrivateServer.objects.all(), id=request.data.get('private_server_id'))
    ip = get_valid_ip(private_server)
    if ip is None:
        return Response('no valid ip', status=status.HTTP_400_BAD_REQUEST)
    
    input_user_id = request.data.get('user_id')
    user = None
    if input_user_id is not None and input_user_id != '':
        request.data.pop('user_id')
        user = get_object_or_404(AppUser, id=input_user_id)
    serializer = PrivateServerVMDeploySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    server_vm: PrivateServerVM = serializer.save()
    server_vm.ip = ip.ip
    server_vm.proxmox_ip = ip
    ip.is_reserved = True
    ip.save()
    server_vm.save()
    if user:
        user.private_server_vm = server_vm
        user.save()
    task = handle_proxmox_deploy.delay(server_vm.id, request.user.id)
    return Response(f'{task.id}')


@extend_schema(
    request=None,
    responses=inline_serializer('private_server_vm_count', fields={'res': serializers.IntegerField()})
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def count_private_server_vms(request):
    res = PrivateServerVM.objects.all().count()
    return Response({'res': res})
