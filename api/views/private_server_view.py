from django.db import transaction
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.ansible_helpers import ProxmoxCreateTemplate
from api.filters import filter_private_server
from api.helpers import Paginator, sort_queryset, get_model_fields, get_valid_ip
from api.helpers.cloudflare import delete_cloudflare_dns
from api.models import PrivateServer, PublicServerOpenvpnSession, AppUser, PrivateServerVmOpenvpnSession, ServerType
from api.permissions import IsPrivateUser, IsVmUser
from api.serializers import PrivateServerQueryParamsSerializer
from api.serializers import (PrivateServerSerializer, PrivateServerProvisionSerializer,
                             TestPrivateServerConnectionSerializer, ObjectIdSerializer, CreateTemplateSerializer,
                             PrivateServerStatsSerializer,
                             PublicServerOpenvpnSessionSerializer, PrivateServerVmOpenvpnSessionSerializer)
from api.tasks import handle_hardening, handle_create_template


@extend_schema(
    responses={200: PrivateServerSerializer(many=True)},
    request=PrivateServerQueryParamsSerializer
)
@api_view(['POST'])
@permission_classes([IsPrivateUser])
def get_private_servers(request):
    queryset = PrivateServer.objects.all()
    query_params = PrivateServerQueryParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    queryset = filter_private_server(queryset, query_params.data)
    fields = get_model_fields(PrivateServer)
    queryset = sort_queryset(queryset, query_params.data, fields, 'name')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = PrivateServerSerializer(queryset, many=True)
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    responses={200: PrivateServerSerializer},
    request=ObjectIdSerializer
)
@api_view(['POST'])
@permission_classes([IsVmUser])
def get_private_server_by_id(request):
    instance = get_object_or_404(PrivateServer, id=request.data.get('id'))
    serializer = PrivateServerSerializer(instance)
    return Response(serializer.data)


@extend_schema(
    responses={200: PrivateServerSerializer},
    request=PrivateServerSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_private_server(request):
    id = request.data.pop('id', None)

    if id is None or id == '':
        serializer = PrivateServerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        obj = PrivateServer.objects.get(id=id)
        serializer = PrivateServerSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
@transaction.atomic()
def delete_private_server(request):
    obj = get_object_or_404(PrivateServer, id=request.data.get('id'))
    if obj.is_hardened:
        hostname = obj.hostname
        delete_cloudflare_dns(hostname)
    for vm in obj.privateservervm_set.all():
        for session in vm.privateservervmopenvpnsession_set.all():
            if session.user.openvpn_sessions > 0:
                session.user.openvpn_sessions -= 1
                session.user.save()

        for vpn in vm.privateservervpn_set.all():
            for session in vpn.wireguard_clients.all():
                if session.client.wireguard_sessions > 0:
                    session.client.wireguard_sessions -= 1
                    session.client.save()

    obj.delete()
    return Response('Record Successfully Deleted', status=status.HTTP_200_OK)


@extend_schema(
    request=PrivateServerProvisionSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def provision_private_server(request):
    """
    provision a private server \n
    protocol can be 1 meaning OPENVPN or 2 meaning WIREGUARD
    """
    data = PrivateServerProvisionSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    # to do: call ansible code here
    return Response('server provisioned', status=status.HTTP_200_OK)


@extend_schema(
    request=TestPrivateServerConnectionSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def test_private_server_connection(request):
    """
    test connection to a private server either by providing an existing server_id \n
    or by specifying another server details which are: \n
    ip : the server ip \n
    password : ther server password \n
    user : the server username \n
    note: if you provided the server_id the other fields will be ignored so if you want to check using the second way make sure to leave it null
    """

    if request.data.get('id') is not None:
        server = get_object_or_404(PrivateServer, id=request.data.get('id'))
        # test connection
        return Response('tested connection')

    data = TestPrivateServerConnectionSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    # test connection
    return Response('tested connection')


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def connect_to_private_server(request):
    server = get_object_or_404(PrivateServer, request.data.get('id'))
    user = request.user
    server.users.add(user)
    return Response(status=status.HTTP_200_OK)


@extend_schema(
    request=ObjectIdSerializer,
    responses=PrivateServerSerializer,
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def harden_private_server(request):
    server = get_object_or_404(PrivateServer, id=request.data.get('id'))
    task = handle_hardening.delay(
        server_id=str(request.data.get('id')),
        server_type=ServerType.PRIVATE,
        host=server.ip,
        username=server.username,
        password=server.password
    )
    return Response(f'{task.id}')


@extend_schema(
    request=ObjectIdSerializer,
    responses=inline_serializer('ip', fields={'ip': serializers.IPAddressField(protocol='IPv4')}),
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_ip(request):
    server = get_object_or_404(PrivateServer, id=request.data.get('id'))
    ip = get_valid_ip(server)
    ip = ip.ip if ip else None
    return Response({'ip': ip})


@extend_schema(
    request=CreateTemplateSerializer,
    responses=None,
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_template(request):
    serializer = CreateTemplateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    server: PrivateServer = get_object_or_404(PrivateServer, id=request.data.get('private_server_id'))
    task = handle_create_template.delay(
        **serializer.data, host=server.ip,
        username=server.username,
        password=server.password
    )
    return Response(f'{task.id}')


@extend_schema(
    request=None,
    responses=inline_serializer('private_servers_count', fields={'res': serializers.IntegerField()})
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def count_private_servers(request):
    res = PrivateServer.objects.all().count()
    return Response({'res': res})


@extend_schema(
    request=None,
    responses=PrivateServerStatsSerializer
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def private_server_stats(request):
    queryset = PrivateServer.objects.all()
    serializer = PrivateServerStatsSerializer(queryset, many=True)
    return Response(serializer.data)


@extend_schema(
    request=ObjectIdSerializer,
    responses=PublicServerOpenvpnSessionSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_user_public_sessions(request):
    user = get_object_or_404(AppUser, id=request.data.get('id'))
    queryset = PublicServerOpenvpnSession.objects.filter(user=user)
    serializer = PublicServerOpenvpnSessionSerializer(queryset, many=True)
    return Response(serializer.data)


@extend_schema(
    request=ObjectIdSerializer,
    responses=PrivateServerVmOpenvpnSessionSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_user_private_sessions(request):
    user = get_object_or_404(AppUser, id=request.data.get('id'))
    queryset = PrivateServerVmOpenvpnSession.objects.filter(user=user)
    serializer = PrivateServerVmOpenvpnSessionSerializer(queryset, many=True)
    return Response(serializer.data)
