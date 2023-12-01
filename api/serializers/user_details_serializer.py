from collections import OrderedDict

from rest_framework import serializers

from api.models import AppUser


class UserDetailsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user_type = serializers.CharField(source='get_user_type_display', read_only=True)
    user_role = serializers.SerializerMethodField()

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
        ]

    def get_user_role(self, obj) -> str:
        return 'admin' if obj.is_superuser else 'client'


class AccountUpdateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = AppUser
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'user_type',
        ]


class UserDetailsRelatedSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        pass

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret = OrderedDict([('user_' + key if 'user' not in key else key, ret[key]) for key in ret])

        return ret


class UpdateSessionsLimitSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    limit = serializers.IntegerField()