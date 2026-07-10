from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller.config import Configurations
from biller_apps.inventory.dataclasses.request.get_all import InventoryGetAll


class InventoryGetAllSerializer(serializers.Serializer):
    values = serializers.CharField(max_length=100, required=False, default='')
    page_num = serializers.IntegerField(default=1)
    limit = serializers.IntegerField(default=Configurations.pagination_count)
    sort_by = serializers.CharField(max_length=100, required=False, default='item_name')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
    filter_key = serializers.CharField(max_length=100, required=False, default='')
    filter_value = serializers.CharField(max_length=100, required=False, default='')
    shop_code = serializers.CharField(max_length=50, required=False, default='')
    item_code = serializers.CharField(max_length=50, required=False, default='')

    def create(self, validated_data) -> InventoryGetAll:
        return InventoryGetAll(**validated_data)
    
    @staticmethod
    def get_all_parameters():
        return [
            OpenApiParameter(
                name='values', 
                description='Column required with coma separated',
                required=False, 
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name='page_num', 
                description='Page number to get the list of records',
                required=False, 
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name='limit', 
                description='Number of data in a single page', 
                required=False,
                type=OpenApiTypes.STR, 
                location=OpenApiParameter.QUERY,
                default=Configurations.pagination_count
            ),
            OpenApiParameter(
                name='sort_by', 
                description='Field to sort by', 
                required=False,
                type=OpenApiTypes.STR, 
                location=OpenApiParameter.QUERY, 
                default='name'
            ),
            OpenApiParameter(
                name='sort_order', 
                description='Sort by Ascending or Descending',
                required=False,
                location=OpenApiParameter.QUERY,
                type=str, 
                enum=['asc', 'desc']
            ),
            OpenApiParameter(
                name='filter_key', 
                description='Field to filter by (e.g., "item_name")',
                required=False,
                location=OpenApiParameter.QUERY,
                type=str, 
                enum=['item_name', 'branch_name']
            ),
            OpenApiParameter(
                name='filter_value', 
                description='Value for the filter field (e.g., "true" or "false" for "is_active")',
                required=False,
                location=OpenApiParameter.QUERY,
                type=str, 
                enum=['true', 'false']
            )
        ]