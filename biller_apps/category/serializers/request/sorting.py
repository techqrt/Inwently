from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.category.dataclasses.request.sorting import CategoryListRequest


class CategoryListRequestSerializer(serializers.Serializer):
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False)

    def create(self, validated_data) -> CategoryListRequest:
        return CategoryListRequest(**validated_data)

    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(name='sort_order', description='Sort by Ascending or Descending',
                             required=True,
                             location=OpenApiParameter.QUERY,
                             type=str, enum=['asc', 'desc'])
        ]
