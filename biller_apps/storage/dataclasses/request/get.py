from dataclasses import dataclass


@dataclass
class StorageGet:
    bucket_name: str
    file_name: str
    dummy: bool