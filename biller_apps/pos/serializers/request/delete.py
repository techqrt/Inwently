# biller_apps/pos/serializers/request/delete.py
from rest_framework import serializers
from biller_apps.pos.dataclasses.request.delete import POSDelete


class POSDeleteSerializer(serializers.Serializer):
    pos_id = serializers.IntegerField()

    def create(self, validated_data) -> POSDelete:
        return POSDelete(**validated_data)