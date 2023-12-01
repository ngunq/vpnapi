# from api.models.enums import Transport, VPNType
from rest_framework import serializers

class EnumSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj) -> str:
        return obj[1]
    
    def get_id(self, obj) -> str:
        return obj[0]
