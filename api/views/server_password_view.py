from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import serializers
from api.filters import filter_provider
from api.helpers import Paginator, sort_queryset, get_model_fields
from api.models import ApiServerType, PrivateServer, PublicServer, PrivateServerVM

from drf_spectacular.utils import inline_serializer

from api.utils.crypto import decrypt
@extend_schema(
        request=inline_serializer(
            'decrypt_password', 
            fields={'id': serializers.UUIDField(), 'type': serializers.ChoiceField(choices=ApiServerType)}
        )
)
@api_view(['POST'])
def decrypt_password(request):
    """
    server type can be:\n
    1 private\n
    2 public\n
    3 server_vmn\n
    """
    server_type = request.data.get('type')
    if server_type == ApiServerType.PRIVATE:
        server = get_object_or_404(PrivateServer, id=request.data.get('id'))
    
    elif server_type == ApiServerType.PUBLIC:
        server = get_object_or_404(PublicServer, id=request.data.get('id'))
    
    elif server_type == ApiServerType.PRIVATE_VM:
        server = get_object_or_404(PrivateServerVM, id=request.data.get('id'))
    
    else:
        return Response('type error')
    
    return Response({'password': decrypt(server.password)})
