from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.purchase.serializers.request.create import PurchaseSerializer
from biller_apps.purchase.serializers.request.update import PurchaseUpdateSerializer
from biller_apps.purchase.serializers.request.delete import PurchaseDeleteSerializer
from biller_apps.purchase.serializers.request.get import PurchaseGetSerializer
from biller_apps.purchase.serializers.response.get import PurchaseGetDataSerializer
from biller_apps.purchase.serializers.response.get_all import PurchaseDataSerializer
from biller_apps.purchase.views import PurchaseView


class PurchaseViewController:

    @extend_schema(
        description="Add a Single Purchase or Multiple Purchase",
        request=PurchaseSerializer,
        responses=SwaggerPage.response(description=PurchaseView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=PurchaseSerializer,
                           exec_func='PurchaseView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return PurchaseView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Purchases",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=PurchaseDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return PurchaseView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get a Purchase",
        parameters=PurchaseGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=PurchaseGetDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=PurchaseGetSerializer).validate
    def get(request: Request) -> Response:
        return PurchaseView().get_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search a Purchase by name or details",
        parameters=SwaggerPage.search_parameters(
            key_description="The key value can be purchase bill number, supplier name, or item name"),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return PurchaseView().search_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update a Purchase",
        request=PurchaseUpdateSerializer,
        responses=SwaggerPage.response(description=PurchaseView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=PurchaseUpdateSerializer,
                           exec_func='PurchaseView().update_extract(request)').validate
    def update(request: Request) -> Response:
        return PurchaseView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a Purchase",
        parameters=PurchaseGetSerializer.get_parameters(),
        responses=SwaggerPage.response(description=PurchaseView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=PurchaseDeleteSerializer,
                           exec_func='PurchaseView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return PurchaseView().delete_extract(params=request.params, token_payload=request.payload)
