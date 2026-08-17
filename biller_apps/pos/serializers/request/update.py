# biller_apps/pos/serializers/request/update.py
from rest_framework import serializers

from biller_apps.pos.dataclasses.request.update import (
    POSUpdate, POSItemAddEntry, POSItemUpdateEntry,
)


class POSItemAddEntrySerializer(serializers.Serializer):
    item_code = serializers.CharField(max_length=10)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, default=0)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, default=0)

    def create(self, validated_data) -> POSItemAddEntry:
        return POSItemAddEntry(**validated_data)


class POSItemUpdateEntrySerializer(serializers.Serializer):
    pos_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False)
    # No `default=None` on any of these — omitted fields simply don't appear
    # in validated_data, avoiding the InventoryUpdateSerializer ambiguity bug.

    def create(self, validated_data) -> POSItemUpdateEntry:
        return POSItemUpdateEntry(**validated_data)


class POSUpdateSerializer(serializers.Serializer):
    pos_id = serializers.IntegerField()
    items_to_add = POSItemAddEntrySerializer(many=True, required=False, default=list)
    items_to_update = POSItemUpdateEntrySerializer(many=True, required=False, default=list)
    items_to_remove = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list
    )
    discounts = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False)
    discounts_unit = serializers.ChoiceField(choices=["percentage", "flat"], required=False)
    wave_off = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, required=False)
    payment_type = serializers.CharField(max_length=15, required=False)

    def create(self, validated_data) -> POSUpdate:
        items_to_add = [POSItemAddEntry(**e) for e in validated_data.pop("items_to_add", [])]
        items_to_update = [POSItemUpdateEntry(**e) for e in validated_data.pop("items_to_update", [])]
        return POSUpdate(
            items_to_add=items_to_add,
            items_to_update=items_to_update,
            **validated_data,
        )