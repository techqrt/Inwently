from dataclasses import dataclass, field
from typing import List


@dataclass
class ApprovalsGetAllRequest:
    values: str
    limit: int
    page_num: int
    values_list: List[str] = field(init=False)

    def __post_init__(self):
        self.values_list = self.values.split(',') if self.values else []
