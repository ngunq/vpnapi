from rest_framework import serializers


class BaseQueryParamsSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    is_desc = serializers.BooleanField(required=False, default=True)
    items_per_page = serializers.IntegerField(required=False, default=10)
    search_query = serializers.CharField(required=False, default='', allow_null=True, allow_blank=True)
    sort = serializers.CharField(required=False, default='', allow_null=True, allow_blank=True)
