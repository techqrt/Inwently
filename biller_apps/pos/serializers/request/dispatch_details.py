# biller_apps/pos/serializers/request/dispatch_details.py
from rest_framework import serializers
from biller_apps.pos.dataclasses.request.dispatch_details import POSDispatchDetails


class POSDispatchDetailsSerializer(serializers.Serializer):
    pos_id = serializers.IntegerField()
    logistics_company = serializers.CharField(max_length=100)
    logistics_charges = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    def create(self, validated_data) -> POSDispatchDetails:
        return POSDispatchDetails(**validated_data)
