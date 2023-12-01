from rest_framework import serializers

from .base_query_params_serializer import BaseQueryParamsSerializer


class AppUserQueryParamsSerializer(BaseQueryParamsSerializer):
    user_type_filter = serializers.IntegerField(allow_null=True, default=-1)
