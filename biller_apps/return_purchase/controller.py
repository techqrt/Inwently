from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.return_purchase.serializers.request.create import ReturnPurchaseSerializer
from biller_apps.return_purchase.serializers.request.update import ReturnPurchaseUpdateSerializer
from biller_apps.return_purchase.serializers.request.delete import ReturnPurchaseDeleteSerializer
from biller_apps.return_purchase.serializers.request.get import ReturnPurchaseGetSerializer
from biller_apps.return_purchase.serializers.response.get import ReturnPurchaseGetDataSerializer
from biller_apps.return_purchase.serializers.response.get_all import ReturnPurchaseDataSerializer
from biller_apps.return_purchase.views import ReturnPurchaseView


class ReturnPurchaseViewController:

    @extend_schema(
        description="Add a Single Return Purchase or Multiple Return Purchase",
        request=ReturnPurchaseSerializer,
        responses=SwaggerPage.response(description=ReturnPurchaseView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=ReturnPurchaseSerializer,
                           exec_func='ReturnPurchaseView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return ReturnPurchaseView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Return Purchases",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=ReturnPurchaseDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return ReturnPurchaseView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get a Return Purchase",
        parameters=ReturnPurchaseGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=ReturnPurchaseGetDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=ReturnPurchaseGetSerializer).validate
    def get(request: Request) -> Response:
        return ReturnPurchaseView().get_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search a Return Purchase by name or details",
        parameters=SwaggerPage.search_parameters(
            key_description="The key value can be return bill number, supplier name, or item name"),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return ReturnPurchaseView().search_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update a Return Purchase",
        request=ReturnPurchaseUpdateSerializer,
        responses=SwaggerPage.response(description=ReturnPurchaseView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=ReturnPurchaseUpdateSerializer,
                           exec_func='ReturnPurchaseView().update_extract(request)').validate
    def update(request: Request) -> Response:
        return ReturnPurchaseView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a Return Purchase",
        parameters=ReturnPurchaseGetSerializer.get_parameters(),
        responses=SwaggerPage.response(description=ReturnPurchaseView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=ReturnPurchaseDeleteSerializer,
                           exec_func='ReturnPurchaseView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return ReturnPurchaseView().delete_extract(params=request.params, token_payload=request.payload)
