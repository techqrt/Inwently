import datetime
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller.config import Configurations
from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.overview_report.dataclasses.request.get_report_customer import OverviewReportCustomerGet


class OverviewReportCustomerGetSerializer(serializers.Serializer):
    page_num = serializers.IntegerField(default=1)
    limit = serializers.IntegerField(default=Configurations.pagination_count)
    start_date = serializers.DateField(default=datetime.date.today() - datetime.timedelta(days=30))
    end_date = serializers.DateField(default=datetime.date.today())
    sort_by = serializers.CharField(max_length=100, required=False, default='name')
    sort_order = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
    filter_key = serializers.CharField(max_length=100, required=False, default='')
    filter_value = serializers.CharField(max_length=100, required=False, default='')

    def create(self, validated_data) -> OverviewReportCustomerGet:
        return OverviewReportCustomerGet(**validated_data)

    @staticmethod
    def get_parameters():
        return [
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
                name="start_date",
                description="Start date for filtering the reports (default: today - 30 days)",
                required=False,
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name="end_date",
                description="End date for filtering the reports (default: today)",
                required=False,
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY
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
                description='Field to filter by (e.g., "customer_name")',
                required=False,
                location=OpenApiParameter.QUERY,
                type=str,
                enum=['customer_name', 'email_id', 'mobile_number']
            ),
            OpenApiParameter(
                name='filter_value',
                description='Value for the filter field',
                required=False,
                location=OpenApiParameter.QUERY,
                type=str
            )
        ]
