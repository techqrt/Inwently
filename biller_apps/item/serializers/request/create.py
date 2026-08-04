from django.utils import timezone
from rest_framework import serializers

from biller_apps.item.dataclasses.request.create import ItemRequest


class ItemRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=350, required=False, default="", allow_blank=True)
    bar_qr_code = serializers.CharField(max_length=50, required=True,allow_blank=True)
    brand_code = serializers.CharField(max_length=10,required=False, default=None, allow_blank=True)
    category_code = serializers.CharField(max_length=10,required=True)
    supplier_code = serializers.CharField(max_length=10,required=True)
    image_url = serializers.URLField(required=False, default=None, allow_blank=True)
    tax_code = serializers.CharField(max_length=100, required=False, default=None, allow_blank=True)
    hsn_code = serializers.CharField(max_length=100, required=False, default=None, allow_blank=True)

    def create(self, validated_data) -> ItemRequest:
        return ItemRequest(**validated_data)
