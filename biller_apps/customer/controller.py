from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.customer.serializers.request.create import CustomerRequestSerializer
from biller_apps.customer.serializers.request.delete import CustomerDeleteSerializer
from biller_apps.customer.serializers.request.delete_many import CustomerDeleteManySerializer
from biller_apps.customer.serializers.request.get import CustomerGetSerializer

from biller_apps.customer.serializers.request.update import CustomerUpdateSerializer
from biller_apps.customer.serializers.response.get import CustomerGetResponseSerializer
from biller_apps.customer.serializers.response.get_all import CustomerGetAllResponseSerializer
from biller_apps.customer.views import CustomerView


class CustomerViewController:

    @extend_schema(
        description="Add an Customer",
        request=CustomerRequestSerializer,
        responses=SwaggerPage.response(description=CustomerView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=CustomerRequestSerializer,
                           exec_func='CustomerView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return CustomerView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Customers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=CustomerGetAllResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return CustomerView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get a Customer",
        parameters=CustomerGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=CustomerGetResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=CustomerGetSerializer).validate
    def get(request: Request) -> Response:
        return CustomerView().get_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update a Customer",
        request=CustomerUpdateSerializer,
        responses=SwaggerPage.response(description=CustomerView().data_update))
    @api_view(['PUT'])
    @SerializerValidations(serializer=CustomerUpdateSerializer,
                           exec_func='CustomerView().update_extract(request)').validate
    def update(request: Request) -> Response:
        return CustomerView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a Customer",
        parameters=CustomerDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description=CustomerView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=CustomerDeleteSerializer,
                           exec_func='CustomerView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return CustomerView().delete_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search a customer mobile number",
        parameters=SwaggerPage.search_parameters(key_description="mobile number"),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return CustomerView().search_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete multiple customers",
        request=CustomerDeleteManySerializer,
        responses=SwaggerPage.response(description=CustomerView().data_delete)
    )
    @api_view(['PATCH'])
    @SerializerValidations(serializer=CustomerDeleteManySerializer,
                           exec_func='CustomerView().delete_many_extract(request)').validate
    def delete_many(request: Request) -> Response:
        return CustomerView().delete_many_extract(params=request.params, token_payload=request.payload)
