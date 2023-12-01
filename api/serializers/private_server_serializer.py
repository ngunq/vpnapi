from collections import OrderedDict

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import PrivateServer, Provider
from api.models.enums import VPNType
from api.utils.crypto import encrypt
from .provider_serializer import ProviderRelatedSerializer


class PrivateServerSerializer(serializers.ModelSerializer):
    ip = serializers.IPAddressField(protocol="IPv4", required=True)
    id = serializers.UUIDField(required=False)
    provider = ProviderRelatedSerializer(read_only=True)
    provider_id = serializers.UUIDField(write_only=True)
    hostname = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    city = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    country = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    is_hardened = serializers.BooleanField(required=False, allow_null=True)
    status = serializers.BooleanField(default=False, allow_null=True)
    total_ips = serializers.SerializerMethodField(read_only=True)
    consumed_ips = serializers.IntegerField(read_only=True)

    class Meta:
        model = PrivateServer
        fields = ['id', 'username', 'ip', 'name', 'password', 'provider', 'city', 'country',
                  'provider_id', 'is_hardened', 'hostname', 'status', 'proxmox_default_volume',
                  'proxmox_node_name', 'proxmox_default_disk', 'consumed_ips', 'total_ips']

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        id = ret.pop('provider_id')
        provider = get_object_or_404(Provider, id=id)
        ret['provider'] = provider
        ret["password"] = encrypt(ret["password"])
        return ret

    def to_representation(self, instance, related=False):
        res = super().to_representation(instance)
        if related:
            return res

        provider = res.pop('provider')

        for k in provider:
            res[k] = provider[k]

        return res

    def get_total_ips(self, obj) -> int:
        res = obj.proxmoxip_set.all().count()
        return res


class PrivateServerRelatedSerializer(PrivateServerSerializer):
    """
    this is same as PrivateServerSerializer except it returns field names prefixed with private_server_
    for usage in flatten nested serializers
    """

    class Meta(PrivateServerSerializer.Meta):
        pass

    def to_representation(self, instance):
        res = super().to_representation(instance, related=True)
        provider = res.pop('provider')
        res = OrderedDict([('private_server_' + key, res[key]) for key in res])

        for k in provider:
            res[k] = provider[k]
        return res


class PrivateServerProvisionSerializer(serializers.Serializer):
    server_id = serializers.UUIDField(required=True)
    vpn_type = serializers.ChoiceField(choices=VPNType.choices)


class TestPrivateServerConnectionSerializer(serializers.Serializer):
    ip = serializers.IPAddressField(protocol='IPv4', required=True)
    password = serializers.CharField(max_length=128, required=True)
    username = serializers.CharField(max_length=100, required=True)
    id = serializers.UUIDField(required=False)


class CreateTemplateSerializer(serializers.Serializer):
    private_server_id = serializers.UUIDField()
    image_url = serializers.CharField(
        default='https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img')
    image_name = serializers.CharField(default='jammy-server-cloudimg-amd64.img')
    vm_id = serializers.IntegerField(default=9004)
    vm_name = serializers.CharField(default='temp4')
    vm_memory = serializers.IntegerField(default=2048)
    vm_bridge = serializers.CharField(default='vmbr0')
    vm_disk = serializers.CharField(default='local-lvm')


class PrivateServerStatsSerializer(serializers.ModelSerializer):
    total_ips = serializers.SerializerMethodField(read_only=True)
    consumed_ips = serializers.IntegerField(read_only=True)

    class Meta:
        model = PrivateServer
        fields = ['total_ips', 'consumed_ips', 'name']

    def get_total_ips(self, obj) -> int:
        res = obj.proxmoxip_set.all().count()
        return res
