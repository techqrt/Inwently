from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller.config import Configurations
from biller_apps.inventory.dataclasses.request.log_get_all import InventoryLogGetAll


class InventoryLogGetAllSerializer(serializers.Serializer):

    

    page_num = serializers.IntegerField(
        default=1
    )

    limit = serializers.IntegerField(
        default=Configurations.pagination_count
    )

    sort_by = serializers.ChoiceField(
        choices=[
            'change_date',
            'eventtype',
            'status'
        ],
        default='change_date'
    )

    sort_order = serializers.ChoiceField(
        choices=['asc', 'desc'],
        required=False,
        default='desc'
    )

    inventory_code = serializers.CharField(
        max_length=50,
        required=False,
        default=''
    )

    start_date = serializers.DateField(
        required=False,
        allow_null=True,
        default=None
    )

    end_date = serializers.DateField(
        required=False,
        allow_null=True,
        default=None
    )

    eventtype = serializers.ChoiceField(
        choices=[
            'CREATE',
            'UPDATE',
            'BULK_CREATE',
            'BULK_UPDATE'
        ],
        required=False,
        allow_null=True,
        default=None
    )

    status = serializers.ChoiceField(
        choices=[
            'SUCCESS',
            'FAILED'
        ],
        required=False,
        allow_null=True,
        default=None
    )

    batch_id = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
        default=None
    )

    def create(self, validated_data) -> InventoryLogGetAll:
        return InventoryLogGetAll(**validated_data)

    @staticmethod
    def get_all_parameters():
        return [
            OpenApiParameter(
                name='page_num',
                description='Page number to get the list of records',
                required=False,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                default=1
            ),

            OpenApiParameter(
                name='limit',
                description='Number of data in a single page',
                required=False,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                default=20
            ),

            OpenApiParameter(
                name='inventory_code',
                description='Filter inventory logs by inventory code',
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY
            ),

            OpenApiParameter(
                name='start_date',
                description='Filter logs from this date (YYYY-MM-DD)',
                required=False,
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY
            ),

            OpenApiParameter(
                name='end_date',
                description='Filter logs until this date (YYYY-MM-DD)',
                required=False,
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY
            ),

            OpenApiParameter(
                name='eventtype',
                description='Filter by event type',
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                enum=[
                    'CREATE',
                    'UPDATE',
                    'BULK_CREATE',
                    'BULK_UPDATE'
                ]
            ),

            OpenApiParameter(
                name='status',
                description='Filter by status',
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                enum=[
                    'SUCCESS',
                    'FAILED'
                ]
            ),

            OpenApiParameter(
                name='batch_id',
                description='Filter by batch ID',
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY
            ),

            OpenApiParameter(
                name='sort_by',
                description='Field to sort by',
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                enum=[
                    'change_date',
                    'eventtype',
                    'status'
                ],
                default='change_date'
            ),

            OpenApiParameter(
                name='sort_order',
                description='Sort order',
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                enum=[
                    'asc',
                    'desc'
                ],
                default='desc'
            ),
        ]