from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.brand.serializers.request.create import BrandRequestSerializer
from biller_apps.brand.serializers.request.delete import BrandDeleteRequestSerializer
from biller_apps.brand.serializers.request.delete_many import BrandDeleteManySerializer
from biller_apps.brand.serializers.request.update import BrandUpdateRequestSerializer
from biller_apps.brand.serializers.response.get_all import BrandGetAllSerializer
from biller_apps.brand.views import BrandView
from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage


class BrandViewController:

    @extend_schema(
        description="Add an Brand",
        request=BrandRequestSerializer,
        responses=SwaggerPage.response(description=BrandView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=BrandRequestSerializer,
                           exec_func='BrandView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return BrandView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Brand",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=BrandGetAllSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return BrandView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a Brand",
        parameters=BrandDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(description=BrandView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=BrandDeleteRequestSerializer,
                           exec_func='BrandView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return BrandView().delete_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update an Brand",
        request=BrandUpdateRequestSerializer,
        responses=SwaggerPage.response(description=BrandView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=BrandUpdateRequestSerializer,
                           exec_func='BrandView().update_extract(request)').validate
    def update(request: Request) -> Response:
        return BrandView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete multiple brands",
        request=BrandDeleteManySerializer,
        responses=SwaggerPage.response(description=BrandView().data_delete)
    )
    @api_view(['PATCH'])
    @SerializerValidations(serializer=BrandDeleteManySerializer,
                           exec_func='BrandView().delete_many_extract(request)').validate
    def delete_many(request: Request) -> Response:
        return BrandView().delete_many_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search a brand ",
        parameters=SwaggerPage.search_parameters(key_description="Search a brand by name "),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return BrandView().search_extract(params=request.params, token_payload=request.payload)
