from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class ReturnItemDataSerializer(serializers.Serializer):
    returnId = serializers.IntegerField()
    returnCode = serializers.CharField()
    billNumber = serializers.IntegerField()
    supplierName = serializers.CharField()
    organisationId = serializers.IntegerField()
    itemName = serializers.CharField()
    returnReason = serializers.CharField()
    quantity = serializers.FloatField()
    price = serializers.FloatField()
    tax = serializers.FloatField()
    totalPrice = serializers.FloatField()
    createdDateTime = serializers.DateTimeField()


class ReturnItemGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=ReturnItemDataSerializer())


class ReturnItemDataResponseSerializer(APiResponseSerializer):
    data = ReturnItemGetAllSerializer()
