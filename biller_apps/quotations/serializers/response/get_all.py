from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class QuotationDataSerializer(serializers.Serializer):
    quotationId = serializers.IntegerField()
    quotationCode = serializers.CharField()
    supplierName = serializers.CharField()
    organisationId = serializers.IntegerField()
    createdDate = serializers.DateTimeField()
    totalAmount = serializers.FloatField()
    itemName = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)
    brand = serializers.CharField()
    quantity = serializers.FloatField()
    price = serializers.FloatField()
    tax = serializers.FloatField()
    total = serializers.FloatField()
    purchase = serializers.BooleanField()
    sales = serializers.BooleanField()


class QuotationGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=QuotationDataSerializer())


class QuotationDataResponseSerializer(APiResponseSerializer):
    data = QuotationGetAllSerializer()
