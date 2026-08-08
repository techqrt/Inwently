from django.utils import timezone
from rest_framework import serializers

from biller_apps.item.dataclasses.request.update import ItemUpdate


class ItemAttributeSerializer(serializers.Serializer):
    attribute_key = serializers.CharField(max_length=100)
    attribute_value = serializers.CharField(max_length=255)
    attribute_unit = serializers.CharField(max_length=50, required=False, default='', allow_blank=True)


class ItemUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    item_code = serializers.CharField(max_length=10)
    description = serializers.CharField(max_length=350, required=False, default="", allow_blank=True)
    bar_qr_code = serializers.CharField(max_length=50, required=True, allow_blank=True)
    brand_code = serializers.CharField(max_length=10, required=True)
    category_code = serializers.CharField(max_length=10, required=True)
    supplier_code = serializers.CharField(max_length=10, required=True)
    image_url = serializers.URLField(required=False, default=None, allow_blank=True)
    tax_code = serializers.CharField(max_length=100, required=True)
    hsn_code = serializers.CharField(max_length=100, required=True)

    # Packaging / pricing
    no_of_packets = serializers.IntegerField(required=False, default=1, min_value=1)
    sku_code = serializers.CharField(max_length=100, required=False, default="", allow_blank=True)
    plain_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0.00,
                                            min_value=0)
    printed_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0.00,
                                              min_value=0)
    moq = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=1.00, min_value=0)

    # One-to-many. No default here on purpose: if the client omits these keys,
    # they're left out of validated_data entirely, so ItemUpdate falls back to its
    # own default of None -> the model leaves existing attributes/images untouched.
    # Sending an explicit [] means "clear them".
    attributes = ItemAttributeSerializer(many=True, required=False)
    other_images = serializers.ListField(child=serializers.URLField(), required=False)

    def create(self, validated_data) -> ItemUpdate:
        return ItemUpdate(**validated_data)