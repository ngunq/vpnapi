from rest_framework import serializers

from api.models import PrivateServerVmOpenvpnSession
from .private_server_vm_serializer import PrivateServerVMRelatedSerializer
from .user_details_serializer import UserDetailsRelatedSerializer


class PrivateServerVmOpenvpnSessionSerializer(serializers.ModelSerializer):
    user = UserDetailsRelatedSerializer(read_only=True)
    server_vm = PrivateServerVMRelatedSerializer(read_only=True)

    class Meta:
        model = PrivateServerVmOpenvpnSession
        fields = ['id', 'date', 'user', 'server_vm']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = ret.pop('user')
        for k, v in user.items():
            ret[k] = v

        server_vm = ret.pop('server_vm')
        for k, v in server_vm.items():
            ret[k] = v
        return ret
