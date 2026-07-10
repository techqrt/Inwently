from dataclasses import dataclass
from typing import BinaryIO


@dataclass
class BulkItemRequest:
    csv_file: BinaryIO
