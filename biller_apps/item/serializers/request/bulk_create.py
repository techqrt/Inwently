from drf_spectacular.utils import OpenApiParameter, OpenApiTypes
from rest_framework import serializers

from biller_apps.item.dataclasses.request.bulk_create import BulkItemRequest


class BulkItemRequestSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def create(self, validated_data) -> BulkItemRequest:
        return BulkItemRequest(**validated_data)

    @staticmethod
    def get_parameters() -> list:
        return [
            OpenApiParameter(
                name='csv_file',
                description='CSV file containing bulk items. The file should contain the following headers: '
                            '[name, description, bar_qr_code, bar_qr_auto, brand_code, category_code, '
                            'supplier_code, created_time, item_image_url]',
                required=True,
                type=OpenApiTypes.BINARY,
                location=OpenApiParameter.FORM
            ),
        ]
