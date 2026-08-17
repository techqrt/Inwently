# biller_apps/pos/serializers/request/status_change.py
from rest_framework import serializers
from biller_apps.pos.dataclasses.request.status_change import POSStatusChange


class POSStatusChangeSerializer(serializers.Serializer):
    pos_id = serializers.IntegerField()

    def create(self, validated_data) -> POSStatusChange:
        return POSStatusChange(**validated_data)