from dataclasses import dataclass


@dataclass
class DeleteGet:
    bucket_name: str
    file_name: str
