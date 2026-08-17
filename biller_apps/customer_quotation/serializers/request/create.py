# biller_apps/customer_quotation/serializers/request/create.py
from rest_framework import serializers

from biller_apps.customer_quotation.dataclasses.request.create import (
    CustomerQuotationCreate, CustomerQuotationItemCreate,
)


class CustomerQuotationItemCreateSerializer(serializers.Serializer):
    item_code = serializers.CharField(max_length=10)
    quantity = serializers.IntegerField(min_value=1)

    def create(self, validated_data) -> CustomerQuotationItemCreate:
        return CustomerQuotationItemCreate(**validated_data)


class CustomerQuotationCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=120)
    customer_phone = serializers.CharField(max_length=20)
    customer_email = serializers.CharField(max_length=120, required=False, allow_blank=True, default="")
    shop_code = serializers.CharField(max_length=10)
    items = CustomerQuotationItemCreateSerializer(many=True)

    def create(self, validated_data) -> CustomerQuotationCreate:
        items_data = validated_data.pop("items")
        items = [CustomerQuotationItemCreate(**item) for item in items_data]
        return CustomerQuotationCreate(items=items, **validated_data)