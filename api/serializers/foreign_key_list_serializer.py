from rest_framework import serializers


class ForeignKeyListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()


class UsernameListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    username = serializers.CharField()
