from rest_framework import serializers


class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    access_token = serializers.CharField()
    id = serializers.SerializerMethodField()

    def get_id(self, obj) -> str:
        return obj.get('user').id
