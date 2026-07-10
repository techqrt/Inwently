from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.stock_transfer.serializers.request.create import StockTransferSerializer
from biller_apps.stock_transfer.serializers.request.delete import StockTransferDeleteSerializer
from biller_apps.stock_transfer.serializers.request.get import StockTransferGetSerializer
from biller_apps.stock_transfer.serializers.request.update import StockTransferUpdateSerializer
from biller_apps.stock_transfer.serializers.response.get import StockTransferGetDataSerializer
from biller_apps.stock_transfer.serializers.response.get_all import StockTransferDataSerializer
from biller_apps.stock_transfer.views import StockTransferView


class StockTransferViewController:

    @extend_schema(
        description="Create a Single Stock and Multiple Stock Transfer",
        request=StockTransferSerializer,
        responses=SwaggerPage.response(description=StockTransferView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=StockTransferSerializer,
                           exec_func='StockTransferView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return StockTransferView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Pending Stock Transfers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=StockTransferDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_pending_transfers(request: Request) -> Response:
        return StockTransferView().get_pending_transfers(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get a Stock Transfer",
        parameters=StockTransferGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=StockTransferGetDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=StockTransferGetSerializer).validate
    def get(request: Request) -> Response:
        return StockTransferView().get_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Completed Stock Transfers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=StockTransferDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_completed_transfers(request: Request) -> Response:
        return StockTransferView().get_completed_transfers(params=request.params, token_payload=request.payload)
    
    @extend_schema(
        description="Get all Rejected Stock Transfers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=StockTransferDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_rejected_transfers(request: Request) -> Response:
        return StockTransferView().get_rejected_transfers(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search a Stock Transfer by transfer ID or status",
        parameters=SwaggerPage.search_parameters(
            key_description="The key value can be either transfer_id or status"),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return StockTransferView().search_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update a Stock Transfer",
        request=StockTransferUpdateSerializer,
        responses=SwaggerPage.response(description=StockTransferView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=StockTransferUpdateSerializer,
                           exec_func='StockTransferView().update_extract(request)').validate
    def update(request: Request) -> Response:
        return StockTransferView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a Stock Transfer",
        parameters=StockTransferGetSerializer.get_parameters(),
        responses=SwaggerPage.response(description=StockTransferView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=StockTransferDeleteSerializer,
                           exec_func='StockTransferView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return StockTransferView().delete_extract(params=request.params, token_payload=request.payload)