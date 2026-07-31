import base64
import json
import os

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.common.common import Common
# biller_apps.common.minio import MinioConfig
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.storage.dataclasses.request.create import CreateGet
from biller_apps.storage.dataclasses.request.get import StorageGet
from biller_apps.storage.dataclasses.request.upload import UploadGet
from biller_apps.storage.models import Storage
from biller_apps.storage.serializers.request.delete import DeleteGet
from biller_apps.common.local_storage import LocalStorage

class StorageView:
    def __init__(self) -> None:
        self.delete_data = "File deleted successfully"
        self.uploaded_data = "Image uploaded successfully"
        self.created_data = "Bucket created successfully"
        self.file_generate_error = "Error in generating file from base64 encoded data"
        self.failed_delete_file = "Failed to delete existing file"
        self.fetch_data = "Data fetched successfully"
        super().__init__()

    def decode_base64_to_file(self, encoded_string: str, output_file_path: str) -> None:
        try:
            decoded_data = base64.b64decode(encoded_string)
            with open(output_file_path, 'wb') as output_file:
                output_file.write(decoded_data)
        except Exception:
            raise FileExistsError(self.file_generate_error)

    def delete_file(self, file_name: str) -> None:
        try:
            os.remove(file_name)
        except Exception:
            raise FileExistsError(self.failed_delete_file)

    @Common().exception_handler
    def upload_extract(self, params: UploadGet, token_payload: Payload):
        file_status = self.decode_base64_to_file(encoded_string=params.files, output_file_path=params.file_name)
        try:
            LocalStorage().create_bucket(bucket_name=params.bucket_name)
        except Exception:
            pass
            LocalStorage().upload_file(bucket_name=params.bucket_name, file_name=params.file_name,
                                  file_obj=params.file_name)
        base_url = token_payload.present_url.replace('http', 'https').replace('/storage/upload/',
                                                                              '/storage/get/?bucket_name=')
        file_url = base_url + params.bucket_name + '&file_name=' + params.file_name

        data = {'file_url': file_url}
        Storage().create(file_url=file_url)
        self.delete_file(file_name=params.file_name)
        return Response(status=status.HTTP_200_OK,
                        data=Utils.success_response_data(message=self.created_data, data=data))

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: CreateGet):
        LocalStorage().create_bucket(bucket_name=params.bucket_name)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.created_data))

    @Common().exception_handler
    @Publish.status_update
    def delete_extract(self, params: DeleteGet):
        LocalStorage().delete_file(bucket_name=params.bucket_name, file_name=params.file_name)
        file_url = '/' + params.bucket_name + '/' + params.file_name
        Storage.remove(file_url=file_url)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.delete_data))

    @Common().exception_handler
    def get_extract(self, params: StorageGet):
        obj = LocalStorage().get_file(bucket_name=params.bucket_name, file_name=params.file_name)
        if params.dummy:
            return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.fetch_data,data=json.loads(obj.data)))
        response = HttpResponse(obj.data, content_type='image/png')
        return response
