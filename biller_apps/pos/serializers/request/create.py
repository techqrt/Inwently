# biller_apps/pos/serializers/request/create.py — revised
from rest_framework import serializers

from biller_apps.pos.dataclasses.request.create import POSCreate
from biller_apps.pos.serializers.request.update import POSItemAddEntrySerializer
from biller_apps.pos.dataclasses.request.update import POSItemAddEntry


class POSCreateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    shop_code = serializers.CharField(max_length=10)
    customer_quotation_id = serializers.IntegerField(required=False)
    items = POSItemAddEntrySerializer(many=True)

    def create(self, validated_data) -> POSCreate:
        items_data = validated_data.pop("items")
        items = [POSItemAddEntry(**item) for item in items_data]
        return POSCreate(items=items, **validated_data)