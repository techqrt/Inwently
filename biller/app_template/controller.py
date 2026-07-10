from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.app_template.serializers.request.create import AppTemplateRequestSerializer
from biller_apps.app_template.serializers.request.delete import AppTemplateDeleteRequestSerializer
from biller_apps.app_template.serializers.request.delete_many import AppTemplateDeleteManySerializer
from biller_apps.app_template.serializers.request.update import AppTemplateUpdateRequestSerializer
from biller_apps.app_template.serializers.response.get_all import AppTemplateGetAllSerializer
from biller_apps.app_template.views import AppTemplateView
from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.swagger import SwaggerPage


class AppTemplateViewController:

    @extend_schema(
        description="Add an AppTemplate",
        request=AppTemplateRequestSerializer,
        responses=SwaggerPage.response(description=AppTemplateView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=AppTemplateRequestSerializer,
                           exec_func='AppTemplateView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return AppTemplateView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all AppTemplate",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=AppTemplateGetAllSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return AppTemplateView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a AppTemplate",
        parameters=AppTemplateDeleteRequestSerializer.get_parameters(),
        responses=SwaggerPage.response(description=AppTemplateView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=AppTemplateDeleteRequestSerializer,
                           exec_func='AppTemplateView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return AppTemplateView().delete_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update an AppTemplate",
        request=AppTemplateUpdateRequestSerializer,
        responses=SwaggerPage.response(description=AppTemplateView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=AppTemplateUpdateRequestSerializer,
                           exec_func='AppTemplateView().update_extract(request)').validate
    def update(request: Request) -> Response:
        return AppTemplateView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete multiple app_templates",
        request=AppTemplateDeleteManySerializer,
        responses=SwaggerPage.response(description=AppTemplateView().data_delete)
    )
    @api_view(['PATCH'])
    @SerializerValidations(serializer=AppTemplateDeleteManySerializer,
                           exec_func='AppTemplateView().delete_many_extract(request)').validate
    def delete_many(request: Request) -> Response:
        return AppTemplateView().delete_many_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search a app_template ",
        parameters=SwaggerPage.search_parameters(key_description="Search a app_template by name "),
        responses=SwaggerPage.response(response=AppTemplateGetAllSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return AppTemplateView().search_extract(params=request.params, token_payload=request.payload)
