import logging

from django.db import transaction
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.ansible_helpers import WireguardAddClient, WireguardRemoveClient
from api.filters import filter_public_server_vpn
from api.helpers import Paginator, sort_queryset, get_model_fields
from api.helpers.exceptions import AnsibleError
from api.models import PublicServerVPN, PublicServer, PublicServerVpnWireguardClient, AppUser, ServerType
from api.models.enums import VPNType
from api.serializers import PublicServerVpnReadSerializer, ObjectIdSerializer, \
    PublicServerVpnQueryParamsSerializer, PublicServerVpnWireguardWriteSerializer, \
    PublicServerVpnOpenvpnWriteSerializer, PublicServerOpenVpnConfigSerializer, PublicServerVpnWireguardClientSerializer
from api.tasks import handle_public_openvpn_setup, handle_public_vpn_wireguard_setup, handle_wireguard_add_client, \
    handle_wireguard_remove_client

logger = logging.getLogger()


@extend_schema(
    responses={200: PublicServerVpnReadSerializer(many=True)},
    request=PublicServerVpnOpenvpnWriteSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
@transaction.atomic()
def setup_public_server_vpn_openvpn(request):
    server = get_object_or_404(
        PublicServer, id=request.data.get('public_server_id'))
    if server.publicservervpn_set.filter(vpn_type=VPNType.OPENVPN).exists():
        return Response('server already have openvpn installed', status=status.HTTP_400_BAD_REQUEST)
    task = handle_public_openvpn_setup.delay(request.data)
    return Response(f'{task.id}')


@extend_schema(
    responses={200: PublicServerVpnReadSerializer(many=True)},
    request=PublicServerVpnWireguardWriteSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
@transaction.atomic()
def setup_public_server_vpn_wireguard(request):
    server = get_object_or_404(
        PublicServer, id=request.data.get('public_server_id'))
    if server.publicservervpn_set.filter(vpn_type=VPNType.WIREGUARD).exists():
        return Response('server already have wireguard installed', status=status.HTTP_400_BAD_REQUEST)
    task = handle_public_vpn_wireguard_setup.delay(request.data)
    return Response(f'{task.id}')


@extend_schema(
    responses={200: PublicServerVpnReadSerializer(many=True)},
    request=PublicServerVpnQueryParamsSerializer
)
@api_view(['POST'])
def get_public_server_vpns(request):
    queryset = PublicServerVPN.objects.all()

    query_params = PublicServerVpnQueryParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    queryset = filter_public_server_vpn(queryset, query_params.data)
    fields = get_model_fields(PublicServerVPN)
    queryset = sort_queryset(queryset, query_params.data, fields, 'id')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = PublicServerVpnReadSerializer(
        queryset, many=True, context={'request': request})
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    responses={200: PublicServerVpnReadSerializer},
    request=ObjectIdSerializer
)
@api_view(['POST'])
def get_public_server_vpn_by_id(request):
    instance = get_object_or_404(PublicServerVPN, id=request.data.get('id'))
    serializer = PublicServerVpnReadSerializer(
        instance, context={'request': request})
    return Response(serializer.data)


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def delete_public_server_vpn(request):
    obj = get_object_or_404(PublicServerVPN, id=request.data.get('id'))
    obj.delete()
    return Response('Record Successfully Deleted', status=status.HTTP_200_OK)


@extend_schema(
    request=inline_serializer('publicservervpnaddwgclient', fields={
        'user_id': serializers.UUIDField(),
        'public_server_vpn_id': serializers.UUIDField()
    }),
    responses=None
)
@api_view(['POST'])
@transaction.atomic()
def public_server_vpn_wireguard_add_client(request):
    user: AppUser = get_object_or_404(AppUser, id=request.data.get('user_id'))
    server_vpn: PublicServerVPN = get_object_or_404(
        PublicServerVPN, id=request.data.get('public_server_vpn_id'))
    if PublicServerVpnWireguardClient.objects.filter(public_server_vpn=server_vpn, client=user).exists():
        return Response('client already added to this server', status=status.HTTP_400_BAD_REQUEST)
    if user.wireguard_sessions == user.wireguard_sessions_limit:
        return Response('client wireguard limit exceeded', status=status.HTTP_400_BAD_REQUEST)

    instance = PublicServerVpnWireguardClient.objects.create(
        public_server_vpn=server_vpn, client=user)

    # Call API Logic here

    data = request.post()

    # Run ansible to update
    task = handle_wireguard_add_client.delay(
        instance.id,
        ServerType.PUBLIC,
        user.id,
        client_username=user.username,
        port=server_vpn.port,
        interface_name=server_vpn.interface_name,
        dns=server_vpn.dns,
        private_ip=server_vpn.private_ip,
        private_subnet_mask=server_vpn.private_subnet_mask,
        keep_alive=server_vpn.keep_alive,
        username=server_vpn.public_server.username,
        host=server_vpn.public_server.ip,
        password=server_vpn.public_server.password,
        hostname=server_vpn.public_server.hostname,
    )

    return Response(f'{task.id}')


@extend_schema(
    request=inline_serializer('publicservervpnremovewgclient', fields={
        'user_id': serializers.UUIDField(),
        'public_server_vpn_id': serializers.UUIDField()
    }),
    responses=None
)
@api_view(['POST'])
@transaction.atomic()
def public_server_vpn_wireguard_remove_client(request):
    user: AppUser = get_object_or_404(AppUser, id=request.data.get('user_id'))
    server_vpn = get_object_or_404(
        PublicServerVPN, id=request.data.get('public_server_vpn_id'))
    if not PublicServerVpnWireguardClient.objects.filter(public_server_vpn=server_vpn, client=user).exists():
        return Response('client is not added to this server', status=status.HTTP_400_BAD_REQUEST)

    instance = PublicServerVpnWireguardClient.objects.get(
        public_server_vpn=server_vpn, client=user)

    task = handle_wireguard_remove_client.delay(
        instance.id,
        ServerType.PUBLIC,
        user.id,
        interface_name=server_vpn.interface_name,
        client_username=user.username,
        host=server_vpn.public_server.ip,
        password=server_vpn.public_server.password,
        hostname=server_vpn.public_server.hostname,
    )

    return Response(f'{task.id}')


@extend_schema(
    request=ObjectIdSerializer,
    responses=PublicServerOpenVpnConfigSerializer
)
@api_view(['POST'])
def get_public_server_vpn_openvpn_config(request):
    server = get_object_or_404(PublicServer, pk=request.data.get('id'))
    serializer = PublicServerOpenVpnConfigSerializer(
        server, context={'request': request})
    return Response(serializer.data)
