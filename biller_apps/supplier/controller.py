from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.supplier.serializers.request.create import SupplierRequestSerializer
from biller_apps.supplier.serializers.request.delete import SupplierDeleteSerializer
from biller_apps.supplier.serializers.request.delete_many import SupplierDeleteManySerializer
from biller_apps.supplier.serializers.request.get import SuppliersGetSerializer
from biller_apps.supplier.serializers.request.update import SupplierUpdateSerializer
from biller_apps.supplier.serializers.response.get import SupplierGetDataSerializer
from biller_apps.supplier.serializers.response.get_all import SupplierDataSerializer
from biller_apps.supplier.views import SupplierView


class SupplierViewController:

    @extend_schema(
        description="Add an Supplier",
        request=SupplierRequestSerializer,
        responses=SwaggerPage.response(description=SupplierView().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=SupplierRequestSerializer,
                           exec_func='SupplierView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return SupplierView().create_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Suppliers",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=SupplierDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return SupplierView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get a Suppliers",
        parameters=SuppliersGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=SupplierGetDataSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SuppliersGetSerializer).validate
    def get(request: Request) -> Response:
        return SupplierView().get_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search a supplier by  name",
        parameters=SwaggerPage.search_parameters(
            key_description="the key value can be either email_id or name of the supplier"),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return SupplierView().search_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Update a Supplier",
        request=SupplierUpdateSerializer,
        responses=SwaggerPage.response(description=SupplierView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=SupplierUpdateSerializer,
                           exec_func='SupplierView().update_extract(request)').validate
    def update(request: Request) -> Response:
        return SupplierView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete a Supplier",
        parameters=SuppliersGetSerializer.get_parameters(),
        responses=SwaggerPage.response(description=SupplierView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=SupplierDeleteSerializer,
                           exec_func='SupplierView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return SupplierView().delete_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete multiple brands",
        request=SupplierDeleteManySerializer,
        responses=SwaggerPage.response(description=SupplierView().data_delete)
    )
    @api_view(['PATCH'])
    @SerializerValidations(serializer=SupplierDeleteManySerializer,
                           exec_func='SupplierView().delete_many_extract(request)').validate
    def delete_many(request: Request) -> Response:
        return SupplierView().delete_many_extract(params=request.params, token_payload=request.payload)
