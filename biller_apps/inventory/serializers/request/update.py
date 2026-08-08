from rest_framework import serializers

from biller_apps.inventory.dataclasses.request.update import InventoryUpdate


class InventoryUpdateSerializer(serializers.Serializer):
    inventory_id = serializers.IntegerField()
    item_code = serializers.CharField(max_length=10, required=False, default=None, allow_null=True)
    shop_code = serializers.CharField(max_length=10, required=False, default=None, allow_null=True)
    expiry_date = serializers.DateField(required=False, default=None, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False, default=None,
                                      allow_null=True)
    balance_qty = serializers.IntegerField(min_value=0, required=False, default=None, allow_null=True)
    store_mapping = serializers.CharField(max_length=100, required=False, default=None, allow_blank=True,
                                           allow_null=True)

    def create(self, validated_data) -> InventoryUpdate:
        return InventoryUpdate(**validated_data)