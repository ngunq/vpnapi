from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.filters import filter_mgmt_whitelisted_ip
from api.helpers import Paginator, sort_queryset, get_model_fields
from api.models import MgmtWhitelistedIp
from api.serializers import MgmtWhitelistedIpSerializer, ObjectIdSerializer, BaseQueryParamsSerializer


@extend_schema(
    responses={200: MgmtWhitelistedIpSerializer},
    request=MgmtWhitelistedIpSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_mgmt_whitelisted_ip(request):
    pk = request.data.pop('id', None)
    if pk is None or pk == '':
        data = request.data
        serializer = MgmtWhitelistedIpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        obj = get_object_or_404(MgmtWhitelistedIp, id=pk)
        serializer = MgmtWhitelistedIpSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: MgmtWhitelistedIpSerializer(many=True)},
    request=BaseQueryParamsSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_mgmt_whitelisted_ips(request):
    queryset = MgmtWhitelistedIp.objects.all()

    query_params = BaseQueryParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    queryset = filter_mgmt_whitelisted_ip(queryset, query_params.data)
    fields = get_model_fields(MgmtWhitelistedIp)
    queryset = sort_queryset(queryset, query_params.data, fields, 'name')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = MgmtWhitelistedIpSerializer(queryset, many=True)
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    responses={200: MgmtWhitelistedIpSerializer},
    request=ObjectIdSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_mgmt_whitelisted_ip_by_id(request):
    instance = get_object_or_404(MgmtWhitelistedIp, id=request.data.get('id'))
    serializer = MgmtWhitelistedIpSerializer(instance)
    return Response(serializer.data)


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def delete_mgmt_whitelisted_ip(request):
    obj = get_object_or_404(MgmtWhitelistedIp, id=request.data.get('id'))
    obj.delete()
    return Response('Record Successfully Deleted', status=status.HTTP_200_OK)
