from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.filters import filter_private_server_user
from api.helpers import Paginator, sort_queryset, get_model_fields
from api.models import PrivateServerUser
from api.serializers import BaseQueryParamsSerializer
from api.serializers import (PrivateServerUserSerializer, ObjectIdSerializer)


@extend_schema(
    responses={200: PrivateServerUserSerializer(many=True)},
    request=BaseQueryParamsSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_private_server_users(request):
    queryset = PrivateServerUser.objects.all()
    query_params = BaseQueryParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    queryset = filter_private_server_user(queryset, query_params.data)
    fields = get_model_fields(PrivateServerUser)
    queryset = sort_queryset(queryset, query_params.data, fields, 'id')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = PrivateServerUserSerializer(queryset, many=True)
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    responses={200: PrivateServerUserSerializer},
    request=PrivateServerUserSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_private_server_user(request):
    pk = request.data.pop('id', None)

    if pk is None or pk == '':
        serializer = PrivateServerUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        obj = get_object_or_404(PrivateServerUser, id=pk)
        serializer = PrivateServerUserSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def delete_private_server_user(request):
    obj = get_object_or_404(PrivateServerUser, id=request.data.get('id'))
    obj.delete()
    return Response('Record Successfully Deleted', status=status.HTTP_200_OK)
