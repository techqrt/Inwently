from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.serializers.request.get_all import GetAllSerializer
from biller_apps.common.serializers.response.search import SearchResponseSerializer
from biller_apps.common.swagger import SwaggerPage
from biller_apps.organisation.serializers.request.create import OrganisationRequestSerializer
from biller_apps.organisation.serializers.request.delete import OrganisationDeleteSerializer
from biller_apps.organisation.serializers.request.delete_many import OrganisationDeleteManyRequest, OrganisationDeleteManySerializer
from biller_apps.organisation.serializers.request.get import OrganisationGetSerializer
from biller_apps.organisation.serializers.response.get import OrganisationGetResponseSerializer
from biller_apps.organisation.serializers.response.get_all import OrganisationGetAllResponseSerializer
from biller_apps.organisation.serializers.request.version import VersionCreateSerializer
from biller_apps.common.serializers.request.search import SearchSerializer

from biller_apps.organisation.views import OrganisationViews


# noinspection PyMethodParameters

class OrganisationViewController:

    @extend_schema(
        description="Creates an Organisation",
        request=OrganisationRequestSerializer,
        responses=SwaggerPage.response(description=OrganisationViews().created_data)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=OrganisationRequestSerializer,
                           exec_func='OrganisationViews().create_extract(request)').validate
    def create(request: Request) -> Response:
        return OrganisationViews().create_extract(params=request.params)

    @extend_schema(
        description="Get an Organisation",
        parameters=OrganisationGetSerializer.get_parameters(),
        responses=SwaggerPage.response(response=OrganisationGetResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=OrganisationGetSerializer).validate
    def get(request: Request) -> Response:
        return OrganisationViews().get_extract(params=request.params)

    @extend_schema(
        description="Get list of Organisation",
        parameters=SwaggerPage.get_all_parameters(),
        responses=SwaggerPage.response(response=OrganisationGetAllResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=GetAllSerializer).validate
    def get_all(request: Request) -> Response:
        return OrganisationViews().get_all_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Delete an Organisation",
        parameters=OrganisationDeleteSerializer.get_parameters(),
        responses=SwaggerPage.response(description=OrganisationViews().delete_data)
    )
    @api_view(['DELETE'])
    @SerializerValidations(serializer=OrganisationDeleteSerializer,
                           exec_func='OrganisationViews().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return OrganisationViews().delete_extract(params=request.params)
    
    @extend_schema(
        description="Delete multiple brands",
        request=OrganisationDeleteManyRequest,
        responses=SwaggerPage.response(description=OrganisationViews().delete_data)
    )
    @api_view(['PATCH'])
    @SerializerValidations(serializer=OrganisationDeleteManySerializer,
                           exec_func='OrganisationViews().delete_many_extract(request)').validate
    def delete_many(request: Request) -> Response:
        return OrganisationViews().delete_many_extract(params=request.params, token_payload=request.payload)


    @extend_schema(
        description="Update an Organisation",
        request=OrganisationRequestSerializer,
        responses=SwaggerPage.response(description=OrganisationViews().update_data)
    )
    @api_view(['PUT'])
    @SerializerValidations(serializer=OrganisationRequestSerializer,
                           exec_func='OrganisationViews().update_extract(request)').validate
    def update(request: Request) -> Response:
        return OrganisationViews().update_extract(params=request.params)

    @extend_schema(
        description="Search a supplier by  name",
        parameters=SwaggerPage.search_parameters(
            key_description="the key value can be either email_id or name of the supplier"),
        responses=SwaggerPage.response(response=SearchResponseSerializer)
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=SearchSerializer).validate
    def search(request: Request) -> Response:
        return OrganisationViews().search_extract(params=request.params, token_payload=request.payload)
    
    @staticmethod
    @extend_schema(
        description="Update Version Details",
        request=VersionCreateSerializer,
        responses=SwaggerPage.response(description=OrganisationViews().data_created)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=VersionCreateSerializer).validate
    def update_version(request: Request) -> Response:
        """Handles POST requests to update version details."""
        return OrganisationViews().create_version_extract(params=request.params)
