from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.taxes.serializers.request.create import TaxesGetSerializer
from biller_apps.taxes.serializers.request.delete_many import TaxesDeleteManyRequestSerializer
from biller_apps.taxes.serializers.request.update import TaxesUpdateRequestSerializer
from biller_apps.taxes.serializers.response.get_all import TaxesGetAllResponseSerializer
from biller_apps.taxes.views import TaxesView


class TaxesViewController:

    @extend_schema(
        description="Add a Tax rates",
        request=TaxesGetSerializer,
        responses=SwaggerPage.response(description=TaxesView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=TaxesGetSerializer,
                           exec_func='TaxesView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return TaxesView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Taxes",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=TaxesGetAllResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return TaxesView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update a Tax rates",
        request=TaxesUpdateRequestSerializer,
        responses=SwaggerPage.response(description=TaxesView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=TaxesUpdateRequestSerializer,
                           exec_func='TaxesView().update_extract(request)').validate
    def update(request: Request) -> Response:
        
        return TaxesView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete many taxes",
        request=TaxesDeleteManyRequestSerializer,
        responses=SwaggerPage.response(description=TaxesView().data_delete)
    )
    @api_view(['PATCH'])
    @SerializerValidations(serializer=TaxesDeleteManyRequestSerializer,
                           exec_func='TaxesView().delete_many_extract(request)').validate
    def delete_many(request: Request) -> Response:
        return TaxesView().delete_many_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search a Taxes ",
        parameters=SwaggerPage.search_parameters(
            key_description="Search using  name of the Taxes"),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return TaxesView().search_extract(params=request.params, token_payload=request.payload)
