from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from biller_apps.common.serializer_validations import SerializerValidations
from biller_apps.common.swagger import SwaggerPage
from biller_apps.storage.serializers.request.create import CreateGetSerializer
from biller_apps.storage.serializers.request.delete import DeleteGetSerializer
from biller_apps.storage.serializers.request.get import StorageGetSerializer
from biller_apps.storage.serializers.request.upload import UploadGetSerializer
from biller_apps.storage.views import StorageView


# noinspection PyMethodParameters
class StorageViewController:

    @extend_schema(
        description="Upload an Image to minio",
        request=UploadGetSerializer,
        responses=SwaggerPage.response(description=StorageView().uploaded_data)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=UploadGetSerializer,
                           exec_func='StorageView().upload_extract(request)').validate
    def upload(request: Request) -> Response:
        return StorageView().upload_extract(params=request.params, token_payload=request.payload)

    @extend_schema(
        description="Create a bucket in minio",
        request=CreateGetSerializer,
        responses=SwaggerPage.response(description=StorageView().created_data)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=CreateGetSerializer,
                           exec_func='StorageView().create_extract(request)').validate
    def create(request: Request) -> Response:
        return StorageView().create_extract(params=request.params)

    @extend_schema(
        description="Delete a file",
        request=DeleteGetSerializer,
        responses=SwaggerPage.response(description=StorageView().delete_data)
    )
    @api_view(['POST'])
    @SerializerValidations(serializer=DeleteGetSerializer,
                           exec_func='StorageView().delete_extract(request)').validate
    def delete(request: Request) -> Response:
        return StorageView().delete_extract(params=request.params)

    @extend_schema(
        description="Get an image",
        parameters=StorageGetSerializer.get_parameters(),
        responses=SwaggerPage.response(description="Byte data of an image")
    )
    @api_view(['GET'])
    @SerializerValidations(serializer=StorageGetSerializer).validate
    def get(request: Request) -> Response:
        return StorageView().get_extract(params=request.params)
