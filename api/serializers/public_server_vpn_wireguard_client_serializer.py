from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import PublicServerVpnWireguardClient, PublicServerVPN, AppUser
from .public_server_vpn_serializer import PublicServerVpnRelatedReadSerializer
from .user_details_serializer import UserDetailsRelatedSerializer


class PublicServerVpnWireguardClientSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    client_id = serializers.UUIDField(write_only=True)
    public_server_vpn_id = serializers.UUIDField(write_only=True)

    client = UserDetailsRelatedSerializer(read_only=True)
    public_server_vpn = PublicServerVpnRelatedReadSerializer(read_only=True)

    class Meta:
        model = PublicServerVpnWireguardClient
        fields = ['id', 'client_id', 'public_server_vpn_id', 'client', 'public_server_vpn', 'config', 'qr_file']
        read_only_fields = ['config', 'qr_file']

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        public_server_vpn_id = ret.pop('public_server_vpn_id')
        public_server_vpn = get_object_or_404(PublicServerVPN, id=public_server_vpn_id)
        ret['public_server_vpn'] = public_server_vpn

        client_id = ret.pop('client_id')
        client = get_object_or_404(AppUser, id=client_id)
        ret['client'] = client

        return ret

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        client = ret.pop('client')

        for k, v in client.items():
            ret[k] = v

        public_server_vpn = ret.pop('public_server_vpn')
        for k, v in public_server_vpn.items():
            ret[k] = v

        return ret
