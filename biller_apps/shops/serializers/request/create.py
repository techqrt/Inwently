from rest_framework import serializers

from biller_apps.shops.dataclases.request.create import ShopsRequest


class ShopsRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=100, default='branch')
    email_id = serializers.EmailField(required=False, default=None, allow_blank=True)
    mobile_number = serializers.CharField(required=False, default=None, max_length=20, allow_blank=True)
    website = serializers.CharField(required=False, default=None, max_length=150, allow_blank=True)
    alt_mobile_number = serializers.CharField(required=False, default=None, max_length=20, allow_blank=True)

    def create(self, validated_data) -> ShopsRequest:
        return ShopsRequest(**validated_data)
