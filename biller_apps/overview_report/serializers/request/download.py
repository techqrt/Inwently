import datetime
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers

from biller.config import Configurations
from biller_apps.common.serializers.request.get import GetSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.overview_report.dataclasses.request.download import OverviewReportDownload
from biller_apps.common.serializers.request.download import GenerateExcelPDFSerializer



class OverviewReportDownloadSerializer(GenerateExcelPDFSerializer):
    page_num = serializers.IntegerField(default=1)
    limit = serializers.IntegerField(default=Configurations.pagination_count)
    start_date = serializers.DateField(default=datetime.date.today() - datetime.timedelta(days=30))
    end_date = serializers.DateField(default=datetime.date.today())

    def create(self, validated_data) -> OverviewReportDownload:
        return OverviewReportDownload(**validated_data)

    @staticmethod
    def get_parameters():
        parent_parameters = SwaggerPage.get_generate_excel_pdf_parameters()
        parent_parameters.extend([
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
            )
        ])
        return parent_parameters