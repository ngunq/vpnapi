from collections import OrderedDict

from rest_framework import serializers

from api.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = Provider
        fields = ['id', 'name']

class ProviderRelatedSerializer(ProviderSerializer):
    
    class Meta(ProviderSerializer.Meta):
        pass
    
    def to_representation(self, instance):
        res = super().to_representation(instance)
        res = OrderedDict([('provider_'+key, res[key]) for key in res])
        return res
