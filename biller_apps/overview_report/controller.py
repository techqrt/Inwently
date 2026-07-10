from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.swagger import SwaggerPage
from biller_apps.overview_report.serializers.request.get_report_item import OverviewReportItemGetSerializer
from biller_apps.overview_report.serializers.request.get_report_customer import OverviewReportCustomerGetSerializer
from biller_apps.overview_report.serializers.request.get_report_supplier import OverviewReportSupplierGetSerializer
from biller_apps.overview_report.serializers.request.download import OverviewReportDownloadSerializer
from biller_apps.overview_report.serializers.response.get_all import ItemOverviewReportDataSerializer
from biller_apps.overview_report.serializers.response.get_all import CustomerOverviewReportDataSerializer
from biller_apps.overview_report.serializers.response.get_all import SupplierOverviewReportDataSerializer
from biller_apps.overview_report.views import OverviewReportView


class OverviewReportViewController:
    
    @extend_schema(
        description="Get all Item Overview Reports",
        parameters=OverviewReportItemGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=ItemOverviewReportDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=OverviewReportItemGetSerializer).validate
    def get_overview_reports(request: Request) -> Response:
        return OverviewReportView().get_overview_reports(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Customer Overview Reports",
        parameters=OverviewReportCustomerGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=CustomerOverviewReportDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=OverviewReportCustomerGetSerializer).validate
    def get_customer_overview_reports(request: Request) -> Response:
        return OverviewReportView().get_customer_overview_reports(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Supplier Overview Reports",
        parameters=OverviewReportSupplierGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=SupplierOverviewReportDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=OverviewReportSupplierGetSerializer).validate
    def get_supplier_overview_reports(request: Request) -> Response:
        return OverviewReportView().get_supplier_overview_reports(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Download Overview Report (Excel or PDF)",
        parameters=OverviewReportDownloadSerializer.get_parameters(),  
        responses=SwaggerPage.response(response=ItemOverviewReportDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=OverviewReportDownloadSerializer).validate 
    def download_overview_report(request: Request) -> Response:
        return OverviewReportView().download_overview_report(request=request, params=request.params, token_payload=request.payload)