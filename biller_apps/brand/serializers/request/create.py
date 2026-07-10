from rest_framework import serializers

from biller_apps.brand.dataclasses.request.create import BrandRequest


class BrandRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def create(self, validated_data) -> BrandRequest:
        return BrandRequest(**validated_data)
