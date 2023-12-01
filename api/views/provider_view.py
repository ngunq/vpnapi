from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.filters import filter_provider
from api.helpers import Paginator, sort_queryset, get_model_fields
from api.models import Provider
from api.serializers import ProviderSerializer, ObjectIdSerializer, BaseQueryParamsSerializer


@extend_schema(
    responses={200: ProviderSerializer},
    request=ProviderSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_provider(request):
    pk = request.data.pop('id', None)

    if pk is None or pk == '':
        serializer = ProviderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        obj = get_object_or_404(Provider, id=pk)
        serializer = ProviderSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={200: ProviderSerializer(many=True)},
    request=BaseQueryParamsSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_providers(request):
    queryset = Provider.objects.all()

    query_params = BaseQueryParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    queryset = filter_provider(queryset, query_params.data)
    fields = get_model_fields(Provider)
    queryset = sort_queryset(queryset, query_params.data, fields, 'name')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = ProviderSerializer(queryset, many=True)
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    responses={200: ProviderSerializer},
    request=ObjectIdSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_provider_by_id(request):
    instance = get_object_or_404(Provider, id=request.data.get('id'))
    serializer = ProviderSerializer(instance)
    return Response(serializer.data)


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def delete_provider(request):
    obj = get_object_or_404(Provider, id=request.data.get('id'))
    obj.delete()
    return Response('Record Successfully Deleted', status=status.HTTP_200_OK)
