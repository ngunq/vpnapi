from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import PrivateServerUser, AppUser, PrivateServer
from .private_server_serializer import PrivateServerRelatedSerializer
from .user_details_serializer import UserDetailsRelatedSerializer


class PrivateServerUserSerializer(serializers.ModelSerializer):
    private_server = PrivateServerRelatedSerializer(read_only=True)
    user = UserDetailsRelatedSerializer(read_only=True)

    private_server_id = serializers.UUIDField(write_only=True)
    user_id = serializers.UUIDField(write_only=True)
    id = serializers.UUIDField(required=False)

    class Meta:
        model = PrivateServerUser
        fields = ['id', 'private_server', 'user', 'private_server_id', 'user_id']
    
    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        user_id = data.pop('user_id')
        ret['user'] = get_object_or_404(AppUser, id=user_id)

        private_server_id = data.pop('private_server_id')
        ret['private_server'] = get_object_or_404(PrivateServer, id=private_server_id)

        return ret
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        private_server = ret.pop('private_server')
        user = ret.pop('user')

        for k in private_server:
            ret[k] = private_server[k]
        
        for k in user:
            ret[k] = user[k]
        
        return ret