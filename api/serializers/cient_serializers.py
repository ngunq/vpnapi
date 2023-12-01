from rest_framework import serializers

from api.models import PrivateServerVM


class ClientPrivateVmSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='private_server.city')
    country = serializers.CharField(source='private_server.country')

    class Meta:
        model = PrivateServerVM
        fields = ['id','name', 'ip', 'country', 'city']


class SuspendClientSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    suspend = serializers.BooleanField(default=False)
