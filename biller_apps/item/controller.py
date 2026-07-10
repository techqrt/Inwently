from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.item.serializers.request.bulk_create import BulkItemRequestSerializer
from biller_apps.item.serializers.request.create import ItemRequestSerializer
from biller_apps.item.serializers.request.delete import ItemDeleteSerializer
from biller_apps.item.serializers.request.delete_many import ItemDeleteManySerializer
from biller_apps.item.serializers.request.get import ItemGetSerializer
from biller_apps.item.serializers.request.update import ItemUpdateSerializer
from biller_apps.item.serializers.response.create import ItemCreateResponseSerializer
from biller_apps.item.serializers.response.get import ItemGetResponseSerializer
from biller_apps.item.serializers.response.get_all import ItemGetAllResponseSerializer
from biller_apps.item.views import ItemView


# noinspection PyMethodParameters

class ItemController:

    @extend_schema(
        description="Insert an Item",
        request=ItemRequestSerializer,
        responses=SwaggerPage.response(response=ItemCreateResponseSerializer)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=ItemRequestSerializer,
                           exec_func='ItemView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return ItemView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Bulk Create Items via CSV",
        request=BulkItemRequestSerializer,
        responses=SwaggerPage.response(description="Bulk Items Created Successfully")
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=BulkItemRequestSerializer,
                           exec_func='ItemView().bulk_create_from_csv(request)').validate
    def bulk_create(request: Request) -> Response:
        return ItemView().bulk_create_extract(request.params, request.payload)

    @extend_schema(
        description="Update an Item",
        request=ItemUpdateSerializer,
        responses=SwaggerPage.response(description=ItemView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=ItemUpdateSerializer,
                           exec_func='ItemView().update_extract(request)').validate
    def update(request: Request) -> Response:
        return ItemView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete an Item",
        parameters=ItemDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description=ItemView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=ItemDeleteSerializer,
                           exec_func='ItemView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return ItemView().delete_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get the Items",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=ItemGetAllResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return ItemView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search an Items",
        parameters=SwaggerPage.search_parameters(key_description="Search using item_code or name"),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return ItemView().search_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete multiple items",
        request=ItemDeleteManySerializer,
        responses=SwaggerPage.response(description=ItemView().data_delete)
    )
    @api_view(['PATCH'])
    @SerializerValidations(serializer=ItemDeleteManySerializer,
                           exec_func='ItemView().delete_many_extract(request)').validate
    def delete_many(request: Request) -> Response:
        return ItemView().delete_many_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get an Item",
        parameters=ItemGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=ItemGetResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=ItemGetSerializer).validate
    def get(request: Request) -> Response:
        return ItemView().get_extract(params=request.params, token_payload=request.payload)
