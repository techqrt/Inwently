# biller_apps/pos/serializers/request/get.py
from rest_framework import serializers
from biller_apps.pos.dataclasses.request.get import POSGet


class POSGetSerializer(serializers.Serializer):
    pos_id = serializers.IntegerField(required=False)
    pos_code = serializers.CharField(required=False)

    def create(self, validated_data) -> POSGet:
        return POSGet(**validated_data)

    # NOTE: InventoryGetSerializer.get_parameters() is referenced in
    # InventoryViewController but its implementation was never shown to me.
    # Omitted here deliberately rather than guessed — see call-site note below.