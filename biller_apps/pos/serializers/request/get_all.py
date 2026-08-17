# biller_apps/pos/serializers/request/get_all.py
from rest_framework import serializers
from biller_apps.pos.dataclasses.request.get_all import POSGetAll


class POSGetAllSerializer(serializers.Serializer):
    page_num = serializers.IntegerField(min_value=1, default=1)
    limit = serializers.IntegerField(min_value=1, max_value=100, default=20)
    is_executed = serializers.BooleanField(required=False)
    sort_by = serializers.ChoiceField(choices=["created_date", "amount"], default="created_date")
    sort_order = serializers.ChoiceField(choices=["asc", "desc"], default="desc")

    def create(self, validated_data) -> POSGetAll:
        return POSGetAll(**validated_data)

    # NOTE: same gap as above — InventoryGetAllSerializer.get_all_parameters()
    # not yet shown to me. Omitted rather than guessed.