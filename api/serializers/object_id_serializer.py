from rest_framework import serializers


class ObjectIdSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)


class IdListSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.UUIDField())


class UUIDSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=True)
