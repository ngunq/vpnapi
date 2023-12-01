import logging

from django.core.files import File
from django.db import transaction
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.ansible_helpers import WireguardRemoveClient
from api.filters import filter_private_server_vpn
from api.helpers import Paginator, sort_queryset, get_model_fields
from api.helpers.exceptions import AnsibleError
from api.models import PrivateServerVPN, PrivateServerVM, PrivateServerVpnWireguardClient, AppUser, ServerType
from api.models.enums import VPNType
from api.serializers import PrivateServerVpnReadSerializer, PrivateServerVpnWireguardWriteSerializer, \
    PrivateServerVpnOpenvpnWriteSerializer, ObjectIdSerializer, PrivateServerVpnQueryParamsSerializer, \
    PrivateServerOpenVpnConfigSerializer, PrivateServerVpnWireguardClientSerializer
from api.tasks import handle_privatevm_openvpn_setup, handle_private_vpn_wireguard_setup, handle_wireguard_add_client, \
    handle_wireguard_remove_client

logger = logging.getLogger()


@extend_schema(
    responses={200: PrivateServerVpnReadSerializer(many=True)},
    request=PrivateServerVpnOpenvpnWriteSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def setup_private_server_vpn_openvpn(request):
    server_vm = get_object_or_404(PrivateServerVM, id=request.data.get('private_server_vm_id'))
    if server_vm.privateservervpn_set.filter(vpn_type=VPNType.OPENVPN).exists():
        return Response('server vm already have openvpn installed', status=status.HTTP_400_BAD_REQUEST)
    task = handle_privatevm_openvpn_setup.delay(request.data)
    return Response(f'{task.id}')


@extend_schema(
    responses={200: PrivateServerVpnReadSerializer(many=True)},
    request=PrivateServerVpnWireguardWriteSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def setup_private_server_vpn_wireguard(request):
    server_vm = get_object_or_404(PrivateServerVM, id=request.data.get('private_server_vm_id'))
    if server_vm.privateservervpn_set.filter(vpn_type=VPNType.WIREGUARD).exists():
        return Response('vm already have wireguard installed', status=status.HTTP_400_BAD_REQUEST)
    task = handle_private_vpn_wireguard_setup.delay(request.data)
    return Response(f'{task.id}')


@extend_schema(
    responses={200: PrivateServerVpnReadSerializer(many=True)},
    request=PrivateServerVpnQueryParamsSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_private_server_vpns(request):
    queryset = PrivateServerVPN.objects.all()

    query_params = PrivateServerVpnQueryParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    queryset = filter_private_server_vpn(queryset, query_params.data)
    fields = get_model_fields(PrivateServerVPN)
    queryset = sort_queryset(queryset, query_params.data, fields, 'id')
    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = PrivateServerVpnReadSerializer(queryset, many=True, context={'request': request})
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    responses={200: PrivateServerVpnReadSerializer},
    request=ObjectIdSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_private_server_vpn_by_id(request):
    instance = get_object_or_404(PrivateServerVPN, id=request.data.get('id'))
    serializer = PrivateServerVpnReadSerializer(instance, context={'request': request})
    return Response(serializer.data)


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def delete_private_server_vpn(request):
    obj = get_object_or_404(PrivateServerVPN, id=request.data.get('id'))
    obj.delete()
    return Response('Record Successfully Deleted', status=status.HTTP_200_OK)


@extend_schema(
    request=inline_serializer('privateservervpnaddwgclient', fields={
        'user_id': serializers.UUIDField(),
        'private_server_vpn_id': serializers.UUIDField()
    }),
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
@transaction.atomic()
def private_server_vpn_wireguard_add_client(request):
    user: AppUser = get_object_or_404(AppUser, id=request.data.get('user_id'))
    server_vpn: PrivateServerVPN = get_object_or_404(PrivateServerVPN, id=request.data.get('private_server_vpn_id'))
    if PrivateServerVpnWireguardClient.objects.filter(private_server_vpn=server_vpn, client=user).exists():
        return Response('client already added to this server', status=status.HTTP_400_BAD_REQUEST)

    if user.wireguard_sessions == user.wireguard_sessions_limit:
        return Response('client wireguard limit exceeded', status=status.HTTP_400_BAD_REQUEST)

    instance = PrivateServerVpnWireguardClient.objects.create(private_server_vpn=server_vpn, client=user)
    task = handle_wireguard_add_client.delay(
        instance.id,
        ServerType.PRIVATE,
        user.id,
        client_username=user.username,
        port=server_vpn.port,
        interface_name=server_vpn.interface_name,
        dns=server_vpn.dns,
        private_ip=server_vpn.private_ip,
        private_subnet_mask=server_vpn.private_subnet_mask,
        keep_alive=server_vpn.keep_alive,
        username=server_vpn.private_server_vm.username,
        host=server_vpn.private_server_vm.ip,
        password=server_vpn.private_server_vm.password,
        hostname=server_vpn.private_server_vm.hostname
    )
    return Response(f'{task.id}')



@extend_schema(
    request=inline_serializer('privateservervpnremovewgclient', fields={
        'user_id': serializers.UUIDField(),
        'private_server_vpn_id': serializers.UUIDField()
    }),
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
@transaction.atomic()
def private_server_vpn_wireguard_remove_client(request):
    user: AppUser = get_object_or_404(AppUser, id=request.data.get('user_id'))
    server_vpn = get_object_or_404(PrivateServerVPN, id=request.data.get('private_server_vpn_id'))
    if not PrivateServerVpnWireguardClient.objects.filter(private_server_vpn=server_vpn, client=user).exists():
        return Response('client is not added to this server', status=status.HTTP_400_BAD_REQUEST)

    instance = PrivateServerVpnWireguardClient.objects.get(private_server_vpn=server_vpn, client=user)
    task = handle_wireguard_remove_client.delay(
        instance.id,
        ServerType.PRIVATE,
        user.id,
        interface_name=server_vpn.interface_name,
        client_username=user.username,
        username=server_vpn.private_server_vm.username,
        host=server_vpn.private_server_vm.ip,
        password=server_vpn.private_server_vm.password
    )

    return Response(f'{task.id}')


@extend_schema(
    request=ObjectIdSerializer,
    responses=PrivateServerOpenVpnConfigSerializer
)
@api_view(['POST'])
def get_private_server_vpn_openvpn_config(request):
    server_vm = get_object_or_404(PrivateServerVM, pk=request.data.get('id'))
    serializer = PrivateServerOpenVpnConfigSerializer(server_vm, context={'request': request})
    return Response(serializer.data)
