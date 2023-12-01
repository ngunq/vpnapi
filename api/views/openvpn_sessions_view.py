from django.db.models import Count
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.filters import filter_openvpn_session
from api.helpers import get_model_fields, sort_queryset, Paginator
from api.models import PublicServerOpenvpnSession, PrivateServerVmOpenvpnSession, PublicServer, PrivateServerVM
from api.serializers import PublicServerOpenvpnSessionSerializer, OpenvpnSessionParamsSerializer, \
    PrivateServerVmOpenvpnSessionSerializer, ObjectIdSerializer, OpenvpnSessionsSerializer
from api.tasks import handle_kill_session


@extend_schema(
    responses={200: PublicServerOpenvpnSessionSerializer(many=True)},
    request=OpenvpnSessionParamsSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_public_server_sessions(request):
    queryset = PublicServerOpenvpnSession.objects.all()

    query_params = OpenvpnSessionParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    if query_params.data.get('id'):
        queryset = queryset.filter(server=request.data.get('id'))
        serializer = PublicServerOpenvpnSessionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    queryset = filter_openvpn_session(queryset, query_params.data)
    fields = get_model_fields(PublicServerOpenvpnSession)
    queryset = sort_queryset(queryset, query_params.data, fields, 'date')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = PublicServerOpenvpnSessionSerializer(queryset, many=True)
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    responses={200: PrivateServerVmOpenvpnSessionSerializer(many=True)},
    request=OpenvpnSessionParamsSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_private_server_vm_sessions(request):
    queryset = PrivateServerVmOpenvpnSession.objects.all()

    query_params = OpenvpnSessionParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    if query_params.data.get('id'):
        queryset = queryset.filter(server_vm__private_server=request.data.get('id'))
        serializer = PrivateServerVmOpenvpnSessionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    queryset = filter_openvpn_session(queryset, query_params.data)
    fields = get_model_fields(PrivateServerVmOpenvpnSession)
    queryset = sort_queryset(queryset, query_params.data, fields, 'date')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = PrivateServerVmOpenvpnSessionSerializer(queryset, many=True)
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    responses=None,
    request=ObjectIdSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def kill_public_server_sessions(request):
    session = get_object_or_404(PublicServerOpenvpnSession, id=request.data.get('id'))

    task = handle_kill_session.delay(session.id)

    return Response(f'{task.id}')


@extend_schema(
    responses=None,
    request=ObjectIdSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def kill_private_server_sessions(request):
    session = get_object_or_404(PrivateServerVmOpenvpnSession, id=request.data.get('id'))

    task = handle_kill_session.delay(session.id)

    return Response(f'{task.id}')


@extend_schema(
    request=None,
    responses=inline_serializer('open_vpn_public_sessions_count', fields={'res': serializers.IntegerField()})
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def count_open_vpn_public_sessions(request):
    res = PublicServerOpenvpnSession.objects.all().count()
    return Response({'res': res})


@extend_schema(
    request=None,
    responses=inline_serializer('open_vpn_private_sessions_count', fields={'res': serializers.IntegerField()})
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def count_open_vpn_private_sessions(request):
    res = PrivateServerVmOpenvpnSession.objects.all().count()
    return Response({'res': res})


@extend_schema(
    request=None,
    responses=OpenvpnSessionsSerializer
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def open_vpn_sessions_by_public_server(request):
    queryset = PublicServer.objects.annotate(sessions=Count('publicserveropenvpnsession')).all()
    serializer = OpenvpnSessionsSerializer(queryset, many=True)
    return Response(serializer.data)


@extend_schema(
    request=None,
    responses=OpenvpnSessionsSerializer
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def open_vpn_sessions_by_private_server_vm(request):
    queryset = PrivateServerVM.objects.annotate(sessions=Count('privateservervmopenvpnsession')).all()
    serializer = OpenvpnSessionsSerializer(queryset, many=True)
    return Response(serializer.data)
