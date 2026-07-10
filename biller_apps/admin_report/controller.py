from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.swagger import SwaggerPage
from biller_apps.admin_report.serializers.request.get_employee_report import AdminReportEmployeeGetSerializer
from biller_apps.admin_report.serializers.response.get_all import EmployeeAdminReportDataSerializer
from biller_apps.admin_report.views import AdminReportView


class AdminReportViewController:
    
    @extend_schema(
        description="Get all Employee Admin Reports",
        parameters=AdminReportEmployeeGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=EmployeeAdminReportDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=AdminReportEmployeeGetSerializer).validate
    def get_admin_reports(request: Request) -> Response:
        return AdminReportView().get_admin_reports(params=request.params, token_payload=request.payload)