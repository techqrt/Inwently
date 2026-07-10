from rest_framework import serializers
from biller_apps.return_item.dataclasses.request.create import ReturnItemRequest


class ReturnItemRequestSerializer(serializers.Serializer):
    purchase_bill_number = serializers.CharField()
    supplier_code = serializers.CharField()
    item_code = serializers.CharField()
    return_reason = serializers.CharField(allow_blank=True, required=False)
    quantity = serializers.FloatField()
    price = serializers.FloatField()
    tax = serializers.FloatField()

    def create(self, validated_data) -> ReturnItemRequest:
        return ReturnItemRequest(**validated_data)
