from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class StockTransferDataSerializer(serializers.Serializer):
    transfer_id = serializers.IntegerField()
    transfer_code = serializers.CharField(max_length=10)
    source_shop_id = serializers.IntegerField()
    destination_shop_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    transfer_date_time = serializers.DateTimeField()
    created_date_time = serializers.DateTimeField()
    status = serializers.CharField(max_length=50)
    organisation_id = serializers.IntegerField()
    remarks = serializers.CharField(allow_blank=True, allow_null=True)
    requested_by = serializers.CharField(max_length=100, allow_blank=True, allow_null=True)
    approved_by = serializers.CharField(max_length=100, allow_blank=True, allow_null=True)


class StockTransferGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=StockTransferDataSerializer())


class StockTransferDataSerializer(APiResponseSerializer):
    data = StockTransferGetAllSerializer()
