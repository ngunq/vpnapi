from rest_framework import serializers

from .base_query_params_serializer import BaseQueryParamsSerializer


class PrivateServerClientsQueryParamsSerializer(BaseQueryParamsSerializer):
    user_id = serializers.UUIDField(required=False, allow_null=True)
    vmid = serializers.UUIDField(required=False, allow_null=True)


