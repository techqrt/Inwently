from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.brand.dataclasses.request.delete import BrandDeleteRequest


class BrandDeleteRequestSerializer(serializers.Serializer):
    brand_code = serializers.CharField(max_length=10)

    def create(self, validated_data) -> BrandDeleteRequest:
        return BrandDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(name='brand_code', description='code for that specific brand',
                             required=True, type=OpenApiTypes.EMAIL,
                             location=OpenApiParameter.QUERY)
        ]
