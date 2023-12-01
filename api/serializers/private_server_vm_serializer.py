from collections import OrderedDict

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import PrivateServer
from api.models import PrivateServerVM
from api.utils.crypto import encrypt
from .private_server_serializer import PrivateServerRelatedSerializer
from django.utils.crypto import get_random_string

class PrivateServerVMSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    private_server = PrivateServerRelatedSerializer(read_only=True)
    private_server_id = serializers.UUIDField(write_only=True, required=True)
    ip = serializers.IPAddressField(protocol='IPv4')
    hostname = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = PrivateServerVM
        fields = [
            'id',
            'name',
            'ip',
            'username',
            'password',
            'private_server',
            'private_server_id',
            'is_hardened',
            'hostname',
            'status',
            'vm_name',
            'vm_id',
            'vm_socket',
            'vm_cores',
            'vm_memory',
            'vm_bridge',
            'vm_disk',
        ]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        private_server_id = ret.pop('private_server_id')
        private_server = get_object_or_404(PrivateServer, id=private_server_id)
        ret['private_server'] = private_server
        ret["password"] = encrypt(get_random_string(15))
        return ret

    def to_representation(self, instance, related=False):
        res = super().to_representation(instance)
        if related:
            return res

        private_server = res.pop('private_server')

        for k in private_server:
            res[k] = private_server[k]

        return res


class PrivateServerVMRelatedSerializer(PrivateServerVMSerializer):
    class Meta(PrivateServerVMSerializer.Meta):
        pass

    def to_representation(self, instance, related=False):
        res = super().to_representation(instance, related=True)
        private_server = res.pop('private_server')
        res = OrderedDict([('private_server_vm_' + key, res[key]) for key in res])

        for k in private_server:
            res[k] = private_server[k]
        return res


class PrivateServerVMDeploySerializer(serializers.ModelSerializer):
    private_server_id = serializers.UUIDField(required=True)
    vm_name = serializers.CharField(required=True)
    name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    vm_socket = serializers.IntegerField(default=1)
    vm_cores = serializers.IntegerField(default=2)
    vm_memory = serializers.IntegerField(default=4096)
    vm_bridge = serializers.CharField(default='vmbr0')
    vm_disk = serializers.IntegerField(default=10)
    vm_template = serializers.CharField(default='VM9000')
    user_id = serializers.UUIDField(required=False, allow_null=True)

    class Meta:
        model = PrivateServerVM
        fields = [
            'private_server_id',
            'vm_name',
            'name',
            'vm_socket',
            'vm_cores',
            'vm_memory',
            'vm_bridge',
            'vm_disk',
            'vm_template',
            'user_id'
        ]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        private_server_id = ret.pop('private_server_id')
        private_server = get_object_or_404(PrivateServer, id=private_server_id)
        ret['private_server'] = private_server
        ret["password"] = encrypt(get_random_string(15))
        if ret.get('name') is None or ret.get('name') == '':
            ret['name'] = ret['vm_name']
        return ret
