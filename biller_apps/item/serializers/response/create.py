from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer

class ItemCreateDataSerializer(serializers.Serializer):
    itemCode = serializers.CharField()
    code = serializers.CharField()

class ItemCreateResponseSerializer(APiResponseSerializer):
    data = ItemCreateDataSerializer()
