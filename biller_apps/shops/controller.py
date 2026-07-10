from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.shops.serializers.request.create import ShopsRequestSerializer
from biller_apps.shops.serializers.request.delete import ShopsDeleteSerializer
from biller_apps.shops.serializers.request.delete_many import ShopDeleteManySerializer
from biller_apps.shops.serializers.request.get import ShopGetSerializer
from biller_apps.shops.serializers.request.get_all import ShopGetAllSerializer
from biller_apps.shops.serializers.request.update import ShopsUpdateRequestSerializer
from biller_apps.shops.serializers.response.get import ShopGetRequestSerializer
from biller_apps.shops.serializers.response.get_all import ShopDataSerializer
from biller_apps.shops.views import ShopsView


# noinspection PyMethodParameters
class ShopsViewController:

    @extend_schema(
        description="Add an Shop",
        request=ShopsRequestSerializer,
        responses=SwaggerPage.response(description=ShopsView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=ShopsRequestSerializer,
                           exec_func='ShopsView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return ShopsView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get a Shop",
        parameters=ShopGetAllSerializer.get_parameters(),
        responses=SwaggerPage.response(response=ShopDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=ShopGetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return ShopsView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a shop",
        parameters=ShopsDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description=ShopsView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=ShopsDeleteSerializer,
                           exec_func='ShopsView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return ShopsView().delete_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update a Shop",
        request=ShopsUpdateRequestSerializer,
        responses=SwaggerPage.response(description=ShopsView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=ShopsUpdateRequestSerializer,
                           exec_func='ShopsView().delete_extract(request)').validate
    def update(request: Request) -> Response:
        return ShopsView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search a branch by email_id or name or branch code",
        parameters=SwaggerPage.search_parameters(
            key_description="Search using name "),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return ShopsView().search_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete multiple Shops",
        request=ShopDeleteManySerializer,
        responses=SwaggerPage.response(description=ShopsView().data_delete)
    )
    @api_view(['PATCH'])
    @SerializerValidations(serializer=ShopDeleteManySerializer,
                           exec_func='ShopsView().delete_many_extract(request)').validate
    def delete_many(request: Request) -> Response:
        return ShopsView().delete_many_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get a shop",
        parameters=ShopGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=ShopGetRequestSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=ShopGetSerializer).validate
    def get(request: Request) -> Response:
        return ShopsView().get_extract(params=request.params, token_payload=request.payload)
