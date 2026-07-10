from rest_framework import serializers

from biller_apps.pos.dataclasses.request.create import POSRequest


class POSRequestSerializer(serializers.Serializer):
    billed_by = serializers.EmailField()
    customer_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    quantity = serializers.FloatField()
    price = serializers.FloatField()
    tax = serializers.FloatField()
    discount = serializers.FloatField()
    total = serializers.FloatField()
    shop_code = serializers.CharField(max_length=10)


    def create(self, validated_data) -> POSRequest:
        return POSRequest(**validated_data)


class POSRequestListSerializer(serializers.ListSerializer):
    child = POSRequestSerializer()

    def create(self, validated_data):
        return [POSRequest(**item) for item in validated_data]


class POSSerializer(serializers.Serializer):
    data = POSRequestListSerializer()

    def create(self, validated_data):
        return self.fields['data'].create(validated_data['data'])