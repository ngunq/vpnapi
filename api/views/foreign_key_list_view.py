from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.models import PrivateServer, PublicServer, Provider, PrivateServerVM, AppUser
from api.serializers import ForeignKeyListSerializer, UsernameListSerializer


@extend_schema(
    request=None,
    responses=ForeignKeyListSerializer(many=True)
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_private_server_fks(request):
    queryset = PrivateServer.objects.all()
    serializer = ForeignKeyListSerializer(queryset, many=True)
    return Response(serializer.data)


@extend_schema(
    request=None,
    responses=ForeignKeyListSerializer(many=True)
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_public_server_fks(request):
    queryset = PublicServer.objects.all()
    serializer = ForeignKeyListSerializer(queryset, many=True)
    return Response(serializer.data)


@extend_schema(
    request=None,
    responses=ForeignKeyListSerializer(many=True)
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_provider_fks(request):
    queryset = Provider.objects.all()
    serializer = ForeignKeyListSerializer(queryset, many=True)
    return Response(serializer.data)


@extend_schema(
    request=None,
    responses=ForeignKeyListSerializer(many=True)
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_private_server_vm_fks(request):
    queryset = PrivateServerVM.objects.all()
    serializer = ForeignKeyListSerializer(queryset, many=True)
    return Response(serializer.data)


@extend_schema(
    request=None,
    responses=ForeignKeyListSerializer(many=True)
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_usernames(request):
    queryset = AppUser.objects.all()
    serializer = UsernameListSerializer(queryset, many=True)
    return Response(serializer.data)
