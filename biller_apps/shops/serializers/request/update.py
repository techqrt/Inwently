from rest_framework import serializers

from biller_apps.shops.dataclases.request.update import ShopsUpdateRequest


class ShopsUpdateRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=100)
    shop_code = serializers.CharField(max_length=10)
    email_id = serializers.EmailField(required=False, default='')
    mobile_number = serializers.CharField(max_length=20, required=False, default=None, allow_blank=True)
    alt_mobile_number = serializers.CharField(max_length=20, required=False, default=None, allow_blank=True)
    website = serializers.CharField(required=False, default=None, max_length=150, allow_blank=True)
    type = serializers.CharField(max_length=100, default='branch')

    def create(self, validated_data) -> ShopsUpdateRequest:
        return ShopsUpdateRequest(**validated_data)
