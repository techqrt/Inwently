from rest_framework import serializers

from biller_apps.return_purchase.dataclasses.request.update import ReturnPurchaseUpdate


class ReturnPurchaseUpdateSerializer(serializers.Serializer):
    return_code = serializers.CharField()
    purchase_id = serializers.IntegerField()
    supplier_id = serializers.IntegerField()
    organisation_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    return_reason = serializers.CharField(allow_blank=True, required=False)
    quantity = serializers.FloatField()
    tax = serializers.FloatField()
    total_price = serializers.FloatField()

    def create(self, validated_data) -> ReturnPurchaseUpdate:
        return ReturnPurchaseUpdate(**validated_data)
