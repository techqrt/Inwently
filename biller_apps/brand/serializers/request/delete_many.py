from rest_framework import serializers

from biller_apps.brand.dataclasses.request.delete_many import BrandDeleteManyRequest


class BrandDeleteManySerializer(serializers.Serializer):
    brand_code = serializers.ListField(required=True)

    def create(self, validated_data) -> BrandDeleteManyRequest:
        return BrandDeleteManyRequest(**validated_data)
