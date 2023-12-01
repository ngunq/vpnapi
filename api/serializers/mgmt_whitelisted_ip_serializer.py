from rest_framework import serializers

from api.models import MgmtWhitelistedIp


class MgmtWhitelistedIpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False, allow_null=True)
    ip = serializers.IPAddressField(protocol='IPv4')

    class Meta:
        model = MgmtWhitelistedIp
        fields = [
            'id',
            'name',
            'ip'
        ]
