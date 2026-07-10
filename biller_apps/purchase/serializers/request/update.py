from rest_framework import serializers

from biller_apps.purchase.dataclasses.request.update import PurchaseUpdate


class PurchaseUpdateSerializer(serializers.Serializer):
    purchase_bill_number = serializers.CharField()
    supplier_code = serializers.CharField()
    item_code = serializers.CharField()
    buying_price = serializers.FloatField()
    landing_cost = serializers.FloatField()
    selling_price = serializers.FloatField()
    tax = serializers.FloatField()
    quantity = serializers.FloatField()
    bill_amount = serializers.FloatField()
    purchase_code = serializers.CharField()

    def create(self, validated_data) -> PurchaseUpdate:
        return PurchaseUpdate(**validated_data)
