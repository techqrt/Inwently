from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.approvals.serializers.request.get_all import ApprovalsGetAllSerializer
from biller_apps.approvals.serializers.request.status_change import ApprovalsStatusChangeSerializer
from biller_apps.approvals.serializers.response.get_all_unapproved import ApproverDataResponseSerializer
from biller_apps.approvals.views import ApproverViews
from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.swagger import SwaggerPage


class ApprovalController:
    @extend_schema(
        description="Get all Request for Approvals",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=ApproverDataResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=ApprovalsGetAllSerializer).validate
    def get_all_unapproved(request: Request) -> Response:
        return ApproverViews().get_all_unapproved_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Approve or reject a request ",
        parameters=ApprovalsStatusChangeSerializer.get_parameters(),
        responses=SwaggerPage.response(description=ApproverViews().data_approved)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=ApprovalsStatusChangeSerializer).validate
    def status_change(request: Request):
        return ApproverViews().status_change_extract(params=request.params, token_payload=request.payload)
