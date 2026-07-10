from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class InventoryDataSerializer(serializers.Serializer):
    itemName = serializers.CharField()
    shopName = serializers.CharField()
    expiryDate = serializers.DateField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    balanceQty = serializers.IntegerField()
    organisationName = serializers.CharField()
    createdTime = serializers.DateTimeField()


class InventoryGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=InventoryDataSerializer())


class InventoryDataSerializerResponse(APiResponseSerializer):
    data = InventoryGetAllSerializer()
