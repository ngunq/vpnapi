from rest_framework import serializers

from .base_query_params_serializer import BaseQueryParamsSerializer


class TaskQueryParamsSerializer(BaseQueryParamsSerializer):
    date_filter = serializers.DateField(required=False, allow_null=True)
