from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class ReturnPurchaseDataSerializer(serializers.Serializer):
    returnId = serializers.IntegerField()
    returnCode = serializers.CharField()
    purchaseId = serializers.IntegerField()
    supplierName = serializers.CharField()
    organisationId = serializers.IntegerField()
    itemName = serializers.CharField()
    returnReason = serializers.CharField()
    quantity = serializers.FloatField()
    tax = serializers.FloatField()
    totalPrice = serializers.FloatField()
    createdDateTime = serializers.DateTimeField()


class ReturnPurchaseGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=ReturnPurchaseDataSerializer())


class ReturnPurchaseDataResponseSerializer(APiResponseSerializer):
    data = ReturnPurchaseGetAllSerializer()
