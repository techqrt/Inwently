from minio import Minio
from minio.error import S3Error

from biller.config import Configurations


class MinioConfig:
    def __init__(self):
        self.host = Configurations.minio['host']
        self.access_key = Configurations.minio['access_key']
        self.secret_key = Configurations.minio['secret_key']
        self.secure = False
        self.client = Minio(endpoint=self.host,
                            access_key=self.access_key,
                            secret_key=self.secret_key,
                            secure=self.secure
                            )

    def create_bucket(self, bucket_name: str):
        try:
            self.client.make_bucket(bucket_name)
        except S3Error as err:
            if err.code == 'BucketAlreadyOwnedByYou':
                raise FileExistsError(f"Bucket '{bucket_name}' already owned by you")
            elif err.code == 'BucketAlreadyExists':
                raise FileExistsError(f"Bucket '{bucket_name}' already exists")
            else:
                raise FileExistsError(f"Bucket '{bucket_name}' error")

    def upload_file(self, bucket_name: str, file_name: str, file_obj):
        try:
            self.client.fput_object(bucket_name, file_name, file_obj)
        except Exception as e:
            raise FileExistsError(f"File '{file_name}' was not successfully")

    def delete_file(self, bucket_name: str, file_name: str):
        try:
            self.client.stat_object(bucket_name, file_name)
            self.client.remove_object(bucket_name, file_name)
        except S3Error as err:
            if err.code == 'NoSuchKey':
                raise FileExistsError(f"File '{file_name}' does not exist")
            elif err.code == 'NoSuchBucket':
                raise FileExistsError(f"Bucket '{bucket_name}' does not exist")
            else:
                raise FileExistsError(f"An error occurred while deleting '{file_name}'")

    def get_file(self, bucket_name: str, file_name: str):
        try:
            return self.client.get_object(bucket_name, file_name)
        except Exception:
            raise FileExistsError(f"An error occurred while getting '{file_name}'")
