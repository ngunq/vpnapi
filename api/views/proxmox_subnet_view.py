from drf_spectacular.utils import extend_schema

from api.serializers import ProxmoxIPSerializer, ObjectIdSerializer, BaseQueryParamsSerializer, \
    ProxmoxIPCreateSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.filters import filter_proxmox_subnet
from api.helpers import Paginator, sort_queryset, get_model_fields, get_ip_range
from api.models import ProxmoxIP, PrivateServer
from api.serializers import ProxmoxIPSerializer, ObjectIdSerializer, BaseQueryParamsSerializer, \
    ProxmoxIPCreateSerializer


@extend_schema(
    responses={200: ProxmoxIPSerializer},
    request=ProxmoxIPCreateSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_proxmox_ips(request):
    serializer = ProxmoxIPCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    ips = get_ip_range(serializer.data.get('start'), serializer.data.get('end'))
    res = []
    server = get_object_or_404(PrivateServer, id=serializer.data.get('private_server_id'))
    for ip in ips:
        if ProxmoxIP.objects.filter(private_server=server, ip=ip).exists():
            continue
        data = serializer.data
        data.pop('start')
        data.pop('end')
        data['ip'] = ip
        obj = ProxmoxIPSerializer(data=data)
        obj.is_valid(raise_exception=True)
        res.append(obj.save())
    output = ProxmoxIPSerializer(res, many=True)
    return Response(output.data)


@extend_schema(
    responses={200: ProxmoxIPSerializer(many=True)},
    request=BaseQueryParamsSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_proxmox_subnets(request):
    queryset = ProxmoxIP.objects.all()

    query_params = BaseQueryParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    queryset = filter_proxmox_subnet(queryset, query_params.data)
    fields = get_model_fields(ProxmoxIP)
    queryset = sort_queryset(queryset, query_params.data, fields, 'id')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = ProxmoxIPSerializer(queryset, many=True)
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    responses={200: ProxmoxIPSerializer},
    request=ObjectIdSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_proxmox_subnet_by_id(request):
    instance = get_object_or_404(ProxmoxIP, id=request.data.get('id'))
    serializer = ProxmoxIPSerializer(instance)
    return Response(serializer.data)


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def delete_proxmox_subnet(request):
    obj = get_object_or_404(ProxmoxIP, id=request.data.get('id'))
    if obj.is_reserved:
        return Response('the ip is reserved on a vm', status=status.HTTP_400_BAD_REQUEST)
    obj.delete()
    return Response('Record Successfully Deleted', status=status.HTTP_200_OK)


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def disable_proxmox_ip(request):
    obj = get_object_or_404(ProxmoxIP, id=request.data.get('id'))
    if obj.is_reserved:
        return Response('the ip is reserved on a vm', status=status.HTTP_400_BAD_REQUEST)
    obj.is_disabled = not obj.is_disabled
    obj.save()
    state = ["disabled", "enabled"][obj.is_disabled]
    return Response(f'current state {state}')
