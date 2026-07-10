from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class BrandDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    brandCode = serializers.CharField()


class BrandGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=BrandDataSerializer())


class BrandGetAllResponseSerializer(APiResponseSerializer):
    data = BrandGetAllSerializer()
