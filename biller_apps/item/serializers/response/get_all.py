from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class ItemGetAllSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    code = serializers.CharField()
    isActive = serializers.BooleanField()
    itemCode = serializers.CharField()
    brandCode = serializers.CharField()
    brandName = serializers.CharField()
    categoryName = serializers.CharField()
    categoryCode = serializers.CharField()
    supplierName = serializers.CharField()
    supplierCode = serializers.CharField()
    createdTime = serializers.DateTimeField()
    imageUrl = serializers.URLField()
    taxCode = serializers.CharField()
    hsnCode = serializers.CharField()
    taxName = serializers.CharField()


class ItemGetAllDataSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=ItemGetAllSerializer())


class ItemGetAllResponseSerializer(APiResponseSerializer):
    data = ItemGetAllDataSerializer()
