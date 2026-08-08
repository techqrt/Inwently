from rest_framework import serializers

from biller_apps.inventory.dataclasses.request.create import InventoryCreate


class InventoryCreateSerializer(serializers.Serializer):
    item_code = serializers.CharField(max_length=10)
    shop_code = serializers.CharField(max_length=10)
    expiry_date = serializers.DateField(required=False, allow_null=True, default=None)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    balance_qty = serializers.IntegerField(min_value=0)
    store_mapping = serializers.CharField(max_length=100, required=False, default="", allow_blank=True)

    def create(self, validated_data) -> InventoryCreate:
        return InventoryCreate(**validated_data)