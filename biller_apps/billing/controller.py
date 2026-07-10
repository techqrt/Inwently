from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.billing.serializers.request.create import BillingRequestSerializer
from biller_apps.billing.serializers.request.delete import BillingDeleteSerializer
from biller_apps.billing.serializers.request.get import BillingGetSerializer
from biller_apps.billing.serializers.response.get import BillDataGetResponseSerializer
from biller_apps.billing.serializers.response.get_all import BillDataResponseSerializer
from biller_apps.billing.views import BillingView
from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.swagger import SwaggerPage


class BillingViewController:

    @extend_schema(
        description="Add a Bill",
        request=BillingRequestSerializer,
        responses=SwaggerPage.response(description=BillingView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=BillingRequestSerializer,
                           exec_func='CustomerView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return BillingView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Bills",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=BillDataResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return BillingView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all items in a Bill",
        parameters=BillingGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=BillDataGetResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=BillingGetSerializer).validate
    def get(request: Request) -> Response:
        return BillingView().get_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a Bill",
        parameters=BillingDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description=BillingView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=BillingDeleteSerializer,
                           exec_func='CustomerView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return BillingView().delete_extract(params=request.params, token_payload=request.payload)
