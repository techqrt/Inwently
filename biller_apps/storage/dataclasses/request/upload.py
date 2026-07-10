from dataclasses import dataclass


@dataclass
class UploadGet:
    bucket_name: str
    file_name: str
    files: str
