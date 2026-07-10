from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.quotations.serializers.request.create import QuotationSerializer
from biller_apps.quotations.serializers.request.update import QuotationUpdateSerializer
from biller_apps.quotations.serializers.request.delete import QuotationDeleteSerializer
from biller_apps.quotations.serializers.request.get import QuotationGetSerializer
from biller_apps.quotations.serializers.response.get import QuotationGetDataSerializer
from biller_apps.quotations.serializers.response.get_all import QuotationDataSerializer
from biller_apps.quotations.views import QuotationView


class QuotationViewController:

    @extend_schema(
        description="Add a Single Quotation or Multiple Quotations",
        request=QuotationSerializer,
        responses=SwaggerPage.response(description=QuotationView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=QuotationSerializer,
                           exec_func='QuotationView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return QuotationView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Quotations",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=QuotationDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return QuotationView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get a Quotation",
        parameters=QuotationGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=QuotationGetDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=QuotationGetSerializer).validate
    def get(request: Request) -> Response:
        return QuotationView().get_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search a Quotation by name or details",
        parameters=SwaggerPage.search_parameters(
            key_description="The key value can be quotation code, supplier name, or item name"),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return QuotationView().search_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update a Quotation",
        request=QuotationUpdateSerializer,
        responses=SwaggerPage.response(description=QuotationView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=QuotationUpdateSerializer,
                           exec_func='QuotationView().update_extract(request)').validate
    def update(request: Request) -> Response:
        return QuotationView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a Quotation",
        parameters=QuotationGetSerializer.get_parameters(),
        responses=SwaggerPage.response(description=QuotationView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=QuotationDeleteSerializer,
                           exec_func='QuotationView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return QuotationView().delete_extract(params=request.params, token_payload=request.payload)
