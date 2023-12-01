from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import AppUser, PrivateServerVM
from .private_server_vm_serializer import PrivateServerVMRelatedSerializer
from .user_details_serializer import UserDetailsSerializer
from .user_registeration_serializer import UserRegisterSerializer


class PrivateServerVmUserDetailsSerializer(UserDetailsSerializer):
    private_server_vm = PrivateServerVMRelatedSerializer(read_only=True)

    class Meta:
        model = AppUser
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'user_type',
            'user_role',
            'private_server_vm'
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        private_server_vm = ret.pop('private_server_vm')

        for k in private_server_vm:
            ret[k] = private_server_vm[k]

        return ret


class PrivateServerVmUserRegisterSerializer(UserRegisterSerializer):
    user_type = serializers.HiddenField(default=3)
    private_server_vm_id = serializers.UUIDField(write_only=True)

    # private_server_vm = se
    class Meta:
        model = AppUser
        fields = [
            'first_name',
            'last_name',
            'user_type',
            'private_server_vm_id'
        ]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        private_server_vm_id = ret.pop('private_server_vm_id')
        private_server_vm = get_object_or_404(PrivateServerVM, id=private_server_vm_id)
        ret['private_server_vm'] = private_server_vm
        return ret

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.private_server_vm = self.validated_data.get('private_server_vm')
        user.save()
        return user
