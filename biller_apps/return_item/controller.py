from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.return_item.serializers.request.create import ReturnItemRequestSerializer
from biller_apps.return_item.serializers.request.update import ReturnItemUpdateSerializer
from biller_apps.return_item.serializers.request.delete import ReturnItemDeleteSerializer
from biller_apps.return_item.serializers.request.get import ReturnItemGetSerializer
from biller_apps.return_item.serializers.request.get import ReturnItemGetSerializer
from biller_apps.return_item.serializers.request.get_by_bill import ReturnItemGetByBillSerializer
from biller_apps.return_item.serializers.response.get_all import ReturnItemDataSerializer
from biller_apps.return_item.serializers.response.get import ReturnItemGetDataSerializer
from biller_apps.return_item.views import ReturnItemView


class ReturnItemViewController:

    @extend_schema(
        description="Add a  Return Item",
        request=ReturnItemRequestSerializer,
        responses=SwaggerPage.response(description=ReturnItemView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=ReturnItemRequestSerializer,
                           exec_func='ReturnItemView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return ReturnItemView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Return Items",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=ReturnItemDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return ReturnItemView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get a Return Item",
        parameters=ReturnItemGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=ReturnItemGetDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=ReturnItemGetSerializer).validate
    def get(request: Request) -> Response:
        return ReturnItemView().get_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get Items of the selected Bill Number",
        parameters=ReturnItemGetByBillSerializer.get_parameters(),
        responses=SwaggerPage.response(response=ReturnItemDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=ReturnItemGetByBillSerializer).validate
    def get_by_bill(request: Request) -> Response:
        return ReturnItemView().get_item_by_bill_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search a Return Item by name or details",
        parameters=SwaggerPage.search_parameters(
            key_description="The key value can be bill number, supplier name, or item name"),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return ReturnItemView().search_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update a Return Item",
        request=ReturnItemUpdateSerializer,
        responses=SwaggerPage.response(description=ReturnItemView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=ReturnItemUpdateSerializer,
                           exec_func='ReturnItemView().update_extract(request)').validate
    def update(request: Request) -> Response:
        return ReturnItemView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a Return Item",
        parameters=ReturnItemGetSerializer.get_parameters(),
        responses=SwaggerPage.response(description=ReturnItemView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=ReturnItemDeleteSerializer,
                           exec_func='ReturnItemView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return ReturnItemView().delete_extract(params=request.params, token_payload=request.payload)
