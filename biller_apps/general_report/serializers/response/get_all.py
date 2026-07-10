from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class PurchaseReportDataSerializer(serializers.Serializer):
    report_id = serializers.IntegerField()
    item_name = serializers.CharField(max_length=255)
    supplier_name = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField()
    buying_price = serializers.FloatField()
    landing_cost = serializers.FloatField()
    selling_price = serializers.FloatField()
    tax = serializers.FloatField()
    bill_amount = serializers.FloatField()
    created_date_time = serializers.DateTimeField()


class PurchaseReportGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=PurchaseReportDataSerializer())

class PurchaseReportDataSerializer(APiResponseSerializer):
    data = PurchaseReportGetAllSerializer()

class QuotationReportDataSerializer(serializers.Serializer):
    report_id = serializers.IntegerField()
    quotation_code = serializers.CharField(max_length=100)
    supplier_name = serializers.CharField(max_length=255)
    created_date = serializers.DateField()
    total_amount = serializers.FloatField()
    item_name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500, allow_blank=True, allow_null=True)
    brand = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    quantity = serializers.IntegerField()
    price = serializers.FloatField()
    tax = serializers.FloatField()
    total = serializers.FloatField()
    purchase = serializers.BooleanField()
    sales = serializers.BooleanField()


class QuotationReportGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=QuotationReportDataSerializer())


class QuotationReportDataSerializer(APiResponseSerializer):
    data = QuotationReportGetAllSerializer()
