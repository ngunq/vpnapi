from rest_framework import serializers

from .base_query_params_serializer import BaseQueryParamsSerializer


class PublicServerQueryParamsSerializer(BaseQueryParamsSerializer):
    provider_filter = serializers.CharField(required=False, default='', allow_null=True, allow_blank=True)
    ip_filter = serializers.IPAddressField(required=False, default='', allow_null=True, allow_blank=True)
    is_hardened_filter = serializers.BooleanField(required=False, default=None, allow_null=True)
    status_filter = serializers.BooleanField(required=False, default=None, allow_null=True)

