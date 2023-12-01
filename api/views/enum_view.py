from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.models import UserType
from api.models.enums import VPNType, Transport
from api.serializers import EnumSerializer


@extend_schema(
    request=None,
    responses=EnumSerializer(many=True)   
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_vpn_types(request):
    serializer = EnumSerializer(VPNType.choices, many=True)
    return Response(serializer.data)

@extend_schema(
    request=None,
    responses=EnumSerializer(many=True)    
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_transports(request):
    serializer = EnumSerializer(Transport.choices, many=True)
    return Response(serializer.data)


@extend_schema(
    request=None,
    responses=EnumSerializer(many=True)    
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_types(request):
    serializer = EnumSerializer(UserType.choices, many=True)
    return Response(serializer.data)
