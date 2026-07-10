from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.general_report.serializers.request.get_report import GeneralReportGetSerializer
from biller_apps.general_report.serializers.response.get_all import QuotationReportDataSerializer
from biller_apps.general_report.serializers.response.get_all import PurchaseReportDataSerializer
from biller_apps.general_report.views import GeneralReportView


class GeneralReportViewController:
    
    @extend_schema(
        description="Get all Purchase Reports",
        parameters=GeneralReportGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=PurchaseReportDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GeneralReportGetSerializer).validate
    def get_purchase_reports(request: Request) -> Response:
        return GeneralReportView().get_purchase_reports(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Quotation Reports",
        parameters=GeneralReportGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=QuotationReportDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GeneralReportGetSerializer).validate
    def get_quotation_reports(request: Request) -> Response:
        return GeneralReportView().get_quotation_reports(params=request.params, token_payload=request.payload)