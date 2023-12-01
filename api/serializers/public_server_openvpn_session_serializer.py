from rest_framework import serializers

from api.models import PublicServerOpenvpnSession
from .public_server_serializer import PublicServerRelatedSerializer
from .user_details_serializer import UserDetailsRelatedSerializer


class PublicServerOpenvpnSessionSerializer(serializers.ModelSerializer):
    user = UserDetailsRelatedSerializer(read_only=True)
    server = PublicServerRelatedSerializer(read_only=True)

    class Meta:
        model = PublicServerOpenvpnSession
        fields = ['id', 'date', 'user', 'server']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = ret.pop('user')
        for k, v in user.items():
            ret[k] = v

        server = ret.pop('server')
        for k, v in server.items():
            ret[k] = v
        return ret
