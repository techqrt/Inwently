from rest_framework import serializers

from biller_apps.stock_transfer.dataclasses.request.create import StockTransferRequest


class StockTransferRequestSerializer(serializers.Serializer):
    source_shop_code = serializers.CharField()
    destination_shop_code = serializers.CharField()
    item_code = serializers.CharField()
    quantity = serializers.IntegerField(min_value=0)
    transfer_date_time = serializers.DateTimeField()
    status = serializers.ChoiceField(choices=['Pending', 'Approved', 'Rejected'], default='Pending')
    remarks = serializers.CharField(allow_blank=True, allow_null=True, default='')
    requested_by = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, default='')
    approved_by = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, default='')

    def create(self, validated_data) -> StockTransferRequest:
        return StockTransferRequest(**validated_data)

class StockTransferRequestListSerializer(serializers.ListSerializer):
    child = StockTransferRequestSerializer()

    def create(self, validated_data):
        return [StockTransferRequest(**item) for item in validated_data]
    
class StockTransferSerializer(serializers.Serializer):
    data = StockTransferRequestListSerializer()

    def create(self, validated_data):
        return self.fields['data'].create(validated_data['data'])