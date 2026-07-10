from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.category.serializers.request.create import CategoryRequestSerializer
from biller_apps.category.serializers.request.delete import CategoryDeleteRequestSerializer
from biller_apps.category.serializers.request.delete_many import CategoryDeleteManySerializer
from biller_apps.category.serializers.request.update import CategoryUpdateRequestSerializer
from biller_apps.category.serializers.response.get_all import CategoryGetAllResponseSerializer
from biller_apps.category.views import CategoryView
from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage


class CategoryViewController:

    @extend_schema(
        description="Add an Category",
        request=CategoryRequestSerializer,
        responses=SwaggerPage.response(description=CategoryView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=CategoryRequestSerializer,
                           exec_func='CategoryView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return CategoryView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Category",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=CategoryGetAllResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return CategoryView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a Category",
        parameters=CategoryDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(description=CategoryView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=CategoryDeleteRequestSerializer,
                           exec_func='CategoryView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return CategoryView().delete_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update a Category",
        request=CategoryUpdateRequestSerializer,
        responses=SwaggerPage.response(description=CategoryView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=CategoryUpdateRequestSerializer,
                           exec_func='CategoryView().update_extract(request)').validate
    def update(request: Request) -> Response:
        return CategoryView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete multiple Category",
        request=CategoryDeleteManySerializer,
        responses=SwaggerPage.response(description=CategoryView().data_delete)
    )
    @api_view(['PATCH'])
    @SerializerValidations(serializer=CategoryDeleteManySerializer,
                           exec_func='CategoryView().delete_many_extract(request)').validate
    def delete_many(request: Request) -> Response:
        return CategoryView().delete_many_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search a category ",
        parameters=SwaggerPage.search_parameters(
            key_description="Search using  name of the category"),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return CategoryView().search_extract(params=request.params, token_payload=request.payload)
