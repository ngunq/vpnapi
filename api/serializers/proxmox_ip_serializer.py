from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import ProxmoxIP, PrivateServer
from .private_server_serializer import PrivateServerRelatedSerializer


class ProxmoxIPSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    private_server = PrivateServerRelatedSerializer(read_only=True)
    private_server_id = serializers.UUIDField(write_only=True, required=True)
    is_reserved = serializers.BooleanField(read_only=True)
    is_disabled = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProxmoxIP
        fields = ['id', 'mask', 'gateway', 'private_server', 'private_server_id', 'ip', 'is_reserved', 'is_disabled']

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        id = ret.pop('private_server_id')
        private_server = get_object_or_404(PrivateServer, id=id)
        ret['private_server'] = private_server
        return ret

    def to_representation(self, instance):
        res = super().to_representation(instance)
        private_server = res.pop('private_server')
        for k in private_server:
            res[k] = private_server[k]

        return res


class ProxmoxIPCreateSerializer(serializers.Serializer):
    start = serializers.IPAddressField(protocol='IPv4')
    end = serializers.IPAddressField(protocol='IPv4')
    mask = serializers.IntegerField()
    gateway = serializers.CharField()
    private_server_id = serializers.UUIDField()
