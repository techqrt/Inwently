from rest_framework import serializers

from biller_apps.brand.dataclasses.request.update import BrandUpdateRequest


class BrandUpdateRequestSerializer(serializers.Serializer):
    brand_code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data) -> BrandUpdateRequest:
        return BrandUpdateRequest(**validated_data)
