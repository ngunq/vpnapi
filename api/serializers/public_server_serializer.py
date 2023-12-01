from collections import OrderedDict

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import PublicServer, Provider
from api.models.enums import VPNType
from api.utils.crypto import encrypt
from .provider_serializer import ProviderRelatedSerializer


class PublicServerSerializer(serializers.ModelSerializer):
    ip = serializers.IPAddressField(protocol="IPv4", required=True)
    id = serializers.UUIDField(required=False)
    provider = ProviderRelatedSerializer(read_only=True)
    provider_id = serializers.UUIDField(write_only=True)
    hostname = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    city = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    country = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    is_hardened = serializers.BooleanField(required=False, allow_null=True)
    status = serializers.BooleanField(default=False, allow_null=True)

    class Meta:
        model = PublicServer
        fields = [
            "id",
            "username",
            "ip",
            "password",
            "provider",
            "city",
            "name",
            "country",
            "provider_id",
            "is_hardened",
            "hostname",
            "status",
        ]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        id = ret.pop("provider_id")
        provider = get_object_or_404(Provider, id=id)
        ret["provider"] = provider
        ret["password"] = encrypt(ret["password"])
        return ret

    def to_representation(self, instance, related=False):
        res = super().to_representation(instance)
        if related:
            return res

        provider = res.pop("provider")

        for k in provider:
            res[k] = provider[k]

        return res


class PublicServerRelatedSerializer(PublicServerSerializer):
    class Meta(PublicServerSerializer.Meta):
        pass

    def to_representation(self, instance):
        res = super().to_representation(instance, related=True)
        provider = res.pop("provider")
        res = OrderedDict([("public_server_" + key, res[key]) for key in res])

        for k in provider:
            res[k] = provider[k]
        return res


class PublicServerProvisionSerializer(serializers.Serializer):
    server_id = serializers.UUIDField(required=True)
    vpn_type = serializers.ChoiceField(choices=VPNType.choices)


class TestPublicServerConnectionSerializer(serializers.Serializer):
    ip = serializers.IPAddressField(protocol="IPv4", required=True)
    password = serializers.CharField(max_length=128, required=True)
    username = serializers.CharField(max_length=100, required=True)
    id = serializers.UUIDField(required=False)
