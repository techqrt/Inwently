from rest_framework import serializers

from biller_apps.quotations.dataclasses.request.create import QuotationRequest


class QuotationRequestSerializer(serializers.Serializer):
    supplier_id = serializers.IntegerField()
    organisation_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    description = serializers.CharField(allow_blank=True, required=False)
    brand = serializers.CharField(allow_blank=True, required=False)
    quantity = serializers.FloatField()
    price = serializers.FloatField()
    tax = serializers.FloatField()
    total = serializers.FloatField()
    purchase = serializers.BooleanField()
    sales = serializers.BooleanField()

    def create(self, validated_data) -> QuotationRequest:
        return QuotationRequest(**validated_data)


class QuotationRequestListSerializer(serializers.ListSerializer):
    child = QuotationRequestSerializer()

    def create(self, validated_data):
        return [QuotationRequest(**item) for item in validated_data]


class QuotationSerializer(serializers.Serializer):
    data = QuotationRequestListSerializer()

    def create(self, validated_data):
        return self.fields['data'].create(validated_data['data'])
