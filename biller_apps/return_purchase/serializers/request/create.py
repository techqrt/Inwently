from rest_framework import serializers

from biller_apps.return_purchase.dataclasses.request.create import ReturnPurchaseRequest


class ReturnPurchaseRequestSerializer(serializers.Serializer):
    purchase_id = serializers.IntegerField()
    supplier_id = serializers.IntegerField()
    organisation_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    return_reason = serializers.CharField(allow_blank=True, required=False)
    quantity = serializers.FloatField()
    tax = serializers.FloatField()
    total_price = serializers.FloatField()

    def create(self, validated_data) -> ReturnPurchaseRequest:
        return ReturnPurchaseRequest(**validated_data)

class ReturnPurchaseRequestListSerializer(serializers.ListSerializer):
    child = ReturnPurchaseRequestSerializer()

    def create(self, validated_data):
        return [ReturnPurchaseRequest(**item) for item in validated_data]
    
class ReturnPurchaseSerializer(serializers.Serializer):
    data = ReturnPurchaseRequestListSerializer()

    def create(self, validated_data):
        return self.fields['data'].create(validated_data['data'])