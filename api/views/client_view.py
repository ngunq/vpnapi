from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.models import UserType, AppUser
from api.serializers import ClientPrivateVmSerializer


@extend_schema(
    responses=ClientPrivateVmSerializer,
    request=None
)
@api_view(['GET'])
def get_client_private_vm(request):
    user: AppUser = request.user
    if user.user_type != UserType.PRIVATE_SERVER_VM_USER or user.private_server_vm is None:
        return Response('client does not have private vm', status=status.HTTP_400_BAD_REQUEST)

    serializer = ClientPrivateVmSerializer(user.private_server_vm)
    return Response(serializer.data)


@extend_schema(
    request=None,
    responses=inline_serializer('public_end_users_count', fields={'res': serializers.IntegerField()})
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def count_public_end_users(request):
    res = AppUser.objects.all().filter(user_type=UserType.PUBLIC).count()
    return Response({'res': res})


@extend_schema(
    request=None,
    responses=inline_serializer('count_res', fields={'res': serializers.IntegerField()})
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def count_private_end_users(request):
    res = AppUser.objects.all().filter(user_type=UserType.PRIVATE).count()
    return Response({'res': res})
