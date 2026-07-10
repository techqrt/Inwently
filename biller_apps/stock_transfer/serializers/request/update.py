from rest_framework import serializers

from biller_apps.stock_transfer.dataclasses.request.update import StockTransferUpdate


class StockTransferUpdateSerializer(serializers.Serializer):
    transfer_code = serializers.CharField(max_length=10, required=False, default='', allow_blank=True)
    source_shop_id = serializers.IntegerField()
    destination_shop_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=0)
    transfer_date_time = serializers.DateTimeField()
    status = serializers.ChoiceField(choices=['Pending', 'Approved', 'Rejected'], default='Pending')
    organisation_id = serializers.IntegerField()
    remarks = serializers.CharField(allow_blank=True, allow_null=True, default='')
    requested_by = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, default='')
    approved_by = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, default='')

    def create(self, validated_data) -> StockTransferUpdate:
        return StockTransferUpdate(**validated_data)
