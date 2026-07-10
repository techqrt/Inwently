from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller_apps.brand.dataclasses.request.sorting import BrandListRequest


class BrandListRequestSerializer(serializers.Serializer):
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False)

    def create(self, validated_data) -> BrandListRequest:
        return BrandListRequest(**validated_data)

    @staticmethod
    def get_parameters():
        return [
            OpenApiParameter(name='sort_order', description='Sort by Ascending or Descending',
                             required=True,
                             location=OpenApiParameter.QUERY,
                             type=str, enum=['asc', 'desc'])
        ]
