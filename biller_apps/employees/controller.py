from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.request.search import SearchSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.employees.serializers.request.bulk_status_change import EmployeeBulkStatusChangeSerializer
from biller_apps.employees.serializers.request.create import EmployeesRequestSerializer
from biller_apps.employees.serializers.request.delete import EmployeeDeleteSerializer
from biller_apps.employees.serializers.request.delete_many import EmployeeDeleteManySerializer
from biller_apps.employees.serializers.request.get import EmployeeGetSerializer
from biller_apps.employees.serializers.request.update import EmployeesUpdateRequestSerializer
from biller_apps.employees.serializers.response.get import EmployeesGetResponseSerializer
from biller_apps.employees.serializers.response.get_all import EmployeesGetAllResponseSerializer
from biller_apps.employees.views import EmployeesView


# noinspection PyMethodParameters
class EmployeesViewController:

    @extend_schema(
        description="Add an Employee",
        request=EmployeesRequestSerializer,
        responses=SwaggerPage.response(description=EmployeesView().data_create)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=EmployeesRequestSerializer,
                           exec_func='EmployeesView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return EmployeesView().create_extract(params=request.params, token_payload=request.payload,host=request.get_host())

    @extend_schema(
        description="Update an Employee",
        request=EmployeesUpdateRequestSerializer,
        responses=SwaggerPage.response(description=EmployeesView().data_update)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=EmployeesUpdateRequestSerializer,
                           exec_func='EmployeesView().update_extract(request)').validate
    def update(request: Request) -> Response:
        return EmployeesView().update_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete an Employee",
        parameters=EmployeeDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description=EmployeesView().data_delete)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=EmployeeDeleteSerializer,
                           exec_func='EmployeesView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return EmployeesView().delete_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get an Employee",
        parameters=EmployeeGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=EmployeesGetResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=EmployeeGetSerializer).validate
    def get(request: Request) -> Response:
        return EmployeesView().get_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Get all Employee",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=EmployeesGetAllResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return EmployeesView().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete multiple employees",
        request=EmployeeDeleteManySerializer,
        responses=SwaggerPage.response(description=EmployeesView().data_delete)
    )
    @api_view(['PATCH'])
    @SerializerValidations(serializer=EmployeeDeleteManySerializer,
                           exec_func='EmployeesView().delete_many_extract(request)').validate
    def delete_many(request: Request) -> Response:
        return EmployeesView().delete_many_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Change the status of the employees in bulk",
        request=EmployeeBulkStatusChangeSerializer,
        responses=SwaggerPage.response(description=EmployeesView().bulk_status_update)
    )
    @api_view(['PATCH'])
    @SerializerValidations(serializer=EmployeeBulkStatusChangeSerializer,
                           exec_func='EmployeesView().bulk_status_change_extract(request)').validate
    def bulk_status_change(request: Request) -> Response:
        return EmployeesView().bulk_status_change_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Search an employee",
        parameters=SwaggerPage.search_parameters(key_description="search by name"),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return EmployeesView().search_extract(params=request.params, token_payload=request.payload)
