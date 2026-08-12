from dataclasses import dataclass, field
from typing import Optional


@dataclass
class InventoryLogGetAll:

    page_num: int
    limit: int

    inventory_code: Optional[str] = None

    start_date: Optional[str] = None
    end_date: Optional[str] = None

    eventtype: Optional[str] = None
    status: Optional[str] = None
    batch_id: Optional[str] = None

    sort_by: str = "change_date"
    sort_order: str = "desc"

    values_list: list = field(default_factory=list)

    @property
    def ordering(self) -> str:
        prefix = "-" if self.sort_order == "desc" else ""
        return f"{prefix}{self.sort_by}"