from rest_framework import serializers

from .base_query_params_serializer import BaseQueryParamsSerializer


class OpenvpnSessionParamsSerializer(BaseQueryParamsSerializer):
    id = serializers.UUIDField(required=False, allow_null=True)
