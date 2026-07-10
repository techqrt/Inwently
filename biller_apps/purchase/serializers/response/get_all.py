from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class PurchaseDataSerializer(serializers.Serializer):
    purchaseBillNumber = serializers.CharField()
    supplierName = serializers.CharField()
    itemName = serializers.CharField()
    buyingPrice = serializers.FloatField()
    landingCost = serializers.FloatField()
    sellingPrice = serializers.FloatField()
    tax = serializers.FloatField()
    quantity = serializers.FloatField()
    billAmount = serializers.FloatField()
    createdDateTime = serializers.DateTimeField()


class PurchaseGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=PurchaseDataSerializer())


class PurchaseDataResponseSerializer(APiResponseSerializer):
    data = PurchaseGetAllSerializer()
