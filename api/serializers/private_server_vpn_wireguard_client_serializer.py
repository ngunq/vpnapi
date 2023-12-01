from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import PrivateServerVpnWireguardClient, PrivateServerVPN, AppUser
from .private_server_vpn_serializer import PrivateServerVpnRelatedReadSerializer
from .user_details_serializer import UserDetailsRelatedSerializer


class PrivateServerVpnWireguardClientSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    client_id = serializers.UUIDField(write_only=True)
    private_server_vpn_id = serializers.UUIDField(write_only=True)

    client = UserDetailsRelatedSerializer(read_only=True)
    private_server_vpn = PrivateServerVpnRelatedReadSerializer(read_only=True)

    class Meta:
        model = PrivateServerVpnWireguardClient
        fields = (
            'id', 
            'client_id', 
            'private_server_vpn_id',
            'client',
            'private_server_vpn',
            'config',
            'qr_file'
            )
        read_only_fields = ['config', 'qr_file']

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        private_server_vpn_id = ret.pop('private_server_vpn_id')
        private_server_vpn = get_object_or_404(PrivateServerVPN, id=private_server_vpn_id)
        ret['private_server_vpn'] = private_server_vpn

        client_id = ret.pop('client_id')
        client = get_object_or_404(AppUser, id=client_id)
        ret['client'] = client

        return ret

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        client = ret.pop('client')

        for k, v in client.items():
            ret[k] = v

        private_server_vpn = ret.pop('private_server_vpn')
        for k, v in private_server_vpn.items():
            ret[k] = v

        return ret
