import os
from django.conf import settings


class FileObj:
    """Mimics minio's object.data so get_extract() doesn't need to change."""
    def __init__(self, data: bytes):
        self.data = data


class LocalStorage:
    def __init__(self):
        self.root = settings.MEDIA_ROOT

    def _bucket_path(self, bucket_name: str) -> str:
        return os.path.join(self.root, bucket_name)

    def _file_path(self, bucket_name: str, file_name: str) -> str:
        return os.path.join(self._bucket_path(bucket_name), file_name)

    def create_bucket(self, bucket_name: str):
        bucket_path = self._bucket_path(bucket_name)
        if os.path.isdir(bucket_path):
            raise FileExistsError(f"Bucket '{bucket_name}' already exists")
        try:
            os.makedirs(bucket_path)
        except Exception:
            raise FileExistsError(f"Bucket '{bucket_name}' error")

    def upload_file(self, bucket_name: str, file_name: str, file_obj: str):
        try:
            os.makedirs(self._bucket_path(bucket_name), exist_ok=True)
            dest_path = self._file_path(bucket_name, file_name)
            with open(file_obj, 'rb') as src, open(dest_path, 'wb') as dst:
                dst.write(src.read())
        except Exception:
            raise FileExistsError(f"File '{file_name}' was not successfully")

    def delete_file(self, bucket_name: str, file_name: str):
        bucket_path = self._bucket_path(bucket_name)
        file_path = self._file_path(bucket_name, file_name)
        if not os.path.isdir(bucket_path):
            raise FileExistsError(f"Bucket '{bucket_name}' does not exist")
        if not os.path.isfile(file_path):
            raise FileExistsError(f"File '{file_name}' does not exist")
        try:
            os.remove(file_path)
        except Exception:
            raise FileExistsError(f"An error occurred while deleting '{file_name}'")

    def get_file(self, bucket_name: str, file_name: str) -> FileObj:
        file_path = self._file_path(bucket_name, file_name)
        try:
            with open(file_path, 'rb') as f:
                return FileObj(f.read())
        except Exception:
            raise FileExistsError(f"An error occurred while getting '{file_name}'")