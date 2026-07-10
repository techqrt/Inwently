from rest_framework import serializers

from biller_apps.quotations.dataclasses.request.update import QuotationUpdate


class QuotationUpdateSerializer(serializers.Serializer):
    supplier_id = serializers.IntegerField()
    organisation_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    description = serializers.CharField(allow_blank=True, required=False)
    brand = serializers.CharField(allow_blank=True, required=False)
    quantity = serializers.FloatField()
    quotation_code = serializers.CharField()
    price = serializers.FloatField()
    tax = serializers.FloatField()
    total = serializers.FloatField()
    purchase = serializers.BooleanField()
    sales = serializers.BooleanField()

    def create(self, validated_data) -> QuotationUpdate:
        return QuotationUpdate(**validated_data)
