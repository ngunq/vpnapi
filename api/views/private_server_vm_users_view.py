from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.filters import filter_account
from api.helpers import Paginator, sort_queryset, get_model_fields
from api.models import AppUser, PrivateServerVM, UserType
from api.serializers import BaseQueryParamsSerializer
from api.serializers import (PrivateServerVmUserRegisterSerializer, ObjectIdSerializer,
                             PrivateServerVmUserDetailsSerializer)


@extend_schema(
    responses={200: PrivateServerVmUserDetailsSerializer(many=True)},
    request=BaseQueryParamsSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_private_server_vm_users(request):
    queryset = AppUser.objects.filter(user_type=UserType.PRIVATE_SERVER_VM_USER).all()
    query_params = BaseQueryParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    queryset = filter_account(queryset, query_params.data)
    fields = get_model_fields(AppUser)
    queryset = sort_queryset(queryset, query_params.data, fields, 'username')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = PrivateServerVmUserDetailsSerializer(queryset, many=True)
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(
    responses={200: PrivateServerVmUserDetailsSerializer},
    request=inline_serializer('updateuserprivatevm', fields={
        'user_id': serializers.UUIDField(),
        'private_server_vm_id': serializers.UUIDField()
    })
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_private_server_vm_user(request):
    """
    change user private_vm to the private_vm with private_server_vm_id
    """
    user: AppUser = get_object_or_404(AppUser, id=request.data.get('user_id'))
    server_vm = get_object_or_404(PrivateServerVM, id=request.data.get('private_server_vm_id'))
    user.private_server_vm = server_vm
    user.save()
    serializer = PrivateServerVmUserDetailsSerializer(user)
    return Response(serializer.data)


@extend_schema(
    request=ObjectIdSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def delete_private_server_vm_user(request):
    """
    delete private_server_vm user
    """
    user: AppUser = get_object_or_404(AppUser, id=request.data.get('id'))
    user.delete()
    return Response('user deleted', status=status.HTTP_200_OK)


@extend_schema(
    request=PrivateServerVmUserRegisterSerializer,
    responses=None,
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_private_server_vm_user(request):
    """
    create new user and link it to vm(private_server_vm_id)
    """
    serializer = PrivateServerVmUserRegisterSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.save(request)
    res = PrivateServerVmUserDetailsSerializer(user)
    return Response(res.data)
