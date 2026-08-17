# biller_apps/pos/dataclasses/request/get_all.py
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class POSGetAll:
    page_num: int
    limit: int
    present_url: str = ""
    is_executed: Optional[bool] = None
    sort_by: str = "created_date"
    sort_order: str = "desc"
    values_list: list = field(default_factory=list)

    @property
    def ordering(self) -> str:
        return f"{'-' if self.sort_order == 'desc' else ''}{self.sort_by}"