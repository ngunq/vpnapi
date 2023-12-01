from rest_framework import serializers

from .base_query_params_serializer import BaseQueryParamsSerializer


class PublicServerVpnQueryParamsSerializer(BaseQueryParamsSerializer):
    vpn_type_filter = serializers.IntegerField(allow_null=True, default=-1)
    transport_filter = serializers.IntegerField(allow_null=True, default=-1)
    status_filter = serializers.BooleanField(required=False, default=None, allow_null=True)