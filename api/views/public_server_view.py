from django.db import transaction
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.filters import filter_public_server
from api.helpers import Paginator, sort_queryset, get_model_fields
from api.helpers.cloudflare import delete_cloudflare_dns
from api.models import PublicServer, ServerType
from api.serializers import (PublicServerSerializer, TestPublicServerConnectionSerializer,
                             PublicServerProvisionSerializer,
                             ObjectIdSerializer, PublicServerQueryParamsSerializer)
from api.tasks import handle_hardening


@extend_schema(
    responses={200: PublicServerSerializer(many=True)},
    request=PublicServerQueryParamsSerializer
)
@api_view(['POST'])
# @permission_classes([IsAdminUser])
def get_public_servers(request):
    queryset = PublicServer.objects.all()

    query_params = PublicServerQueryParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    queryset = filter_public_server(queryset, query_params.data)
    fields = get_model_fields(PublicServer)
    queryset = sort_queryset(queryset, query_params.data, fields, 'name')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = PublicServerSerializer(queryset, many=True)
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    responses={200: PublicServerSerializer},
    request=ObjectIdSerializer
)
@api_view(['POST'])
def get_public_server_by_id(request):
    instance = get_object_or_404(PublicServer, id=request.data.get('id'))
    serializer = PublicServerSerializer(instance)
    return Response(serializer.data)


@extend_schema(
    responses={200: PublicServerSerializer},
    request=PublicServerSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_public_server(request):
    pk = request.data.pop('id', None)

    if pk is None or pk == '':
        serializer = PublicServerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        obj = get_object_or_404(PublicServer, id=pk)
        serializer = PublicServerSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=ObjectIdSerializer,
    responses=None,
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
@transaction.atomic()
def delete_public_server(request):
    obj = get_object_or_404(PublicServer, id=request.data.get('id'))
    if obj.is_hardened:
        try:
            hostname = obj.hostname
            delete_cloudflare_dns(hostname)
        except:
            pass

    for session in obj.publicserveropenvpnsession_set.all():
        if session.user.openvpn_sessions > 0:
            session.user.openvpn_sessions -= 1
            session.user.save()

    for vpn in obj.publicservervpn_set.all():
        for client in vpn.wireguard_clients.all():
            if client.wireguard_sessions > 0:
                client.wireguard_sessions -= 1
                client.save()
    obj.delete()
    return Response('Record Successfully Deleted', status=status.HTTP_200_OK)


@extend_schema(
    request=PublicServerProvisionSerializer,
    responses=None,
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def provision_public_server(request):
    """
    provision a public server \n
    protocol can be 1 meaning OPENVPN or 2 meaning WIREGUARD
    """
    data = PublicServerProvisionSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    # to do: call ansible code here
    return Response('server provisioned', status=status.HTTP_200_OK)


@extend_schema(
    request=TestPublicServerConnectionSerializer,
    responses=None,
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def test_public_server_connection(request):
    """
    test connection to a public server either by providing an existing server_id \n
    or by specifying another server details which are: \n
    ip : the server ip \n
    password : ther server password \n
    user : the server username \n
    note: if you provided the server_id the other fields will be ignored so if you want to check using the second way make sure to leave it null
    """

    if request.data.get('id') is not None:
        server = get_object_or_404(PublicServer, id=request.data.get('id'))
        # test connection
        return Response('tested connection')

    data = TestPublicServerConnectionSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    # test connection
    return Response('tested connection')


@extend_schema(
    request=ObjectIdSerializer,
    responses=None,
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def connect_to_public_server(requset):
    server = get_object_or_404(PublicServer, requset.data.get('id'))
    user = requset.user
    server.users.add(user)
    return Response(status=status.HTTP_200_OK)


@extend_schema(
    request=ObjectIdSerializer,
    responses=PublicServerSerializer,
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def harden_public_server(request):
    server = get_object_or_404(PublicServer, id=request.data.get('id'))

    task = handle_hardening.delay(
        server.id,
        ServerType.PUBLIC,
        host=server.ip,
        username=server.username,
        password=server.password
    )
    return Response(f'{task.id}')


@extend_schema(
    request=None,
    responses=inline_serializer('public_servers_count', fields={'res': serializers.IntegerField()})
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def count_public_servers(request):
    res = PublicServer.objects.all().count()
    return Response({'res': res})
