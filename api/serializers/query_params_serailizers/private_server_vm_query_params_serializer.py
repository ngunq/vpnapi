from rest_framework import serializers

from .base_query_params_serializer import BaseQueryParamsSerializer


class PrivateServerVmQueryParamsSerializer(BaseQueryParamsSerializer):
    is_hardened_filter = serializers.BooleanField(required=False, default=None, allow_null=True)
    status_filter = serializers.BooleanField(required=False, default=None, allow_null=True)

