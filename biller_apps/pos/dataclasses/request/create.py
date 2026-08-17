# biller_apps/pos/dataclasses/request/create.py — revised
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class POSCreate:
    customer_id: int
    shop_code: str
    items: list  # list[POSItemAddEntry]
    customer_quotation_id: Optional[int] = None

    def __post_init__(self):
        self.shop_code = self.shop_code.strip()
        if not self.shop_code:
            raise ValueError("shop_code is required.")
        if not self.items:
            raise ValueError("At least one item is required.")