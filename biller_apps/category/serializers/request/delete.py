from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.category.dataclasses.request.delete import CategoryDeleteRequest


class CategoryDeleteRequestSerializer(serializers.Serializer):
    category_code = serializers.CharField(max_length=50)

    def create(self, validated_data) -> CategoryDeleteRequest:
        return CategoryDeleteRequest(**validated_data)

    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(name='category_code', description='code of the category',
                             required=True, type=OpenApiTypes.EMAIL,
                             location=OpenApiParameter.QUERY)
        ]
