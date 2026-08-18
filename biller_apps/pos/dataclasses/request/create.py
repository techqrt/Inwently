# biller_apps/pos/dataclasses/request/create.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class POSCreate:
    customer_code: str
    shop_code: str
    items: list  # list[POSItemAddEntry]
    customer_quotation_code: Optional[str] = None

    def __post_init__(self):
        self.customer_code = self.customer_code.strip()
        self.shop_code = self.shop_code.strip()
        if self.customer_quotation_code:
            self.customer_quotation_code = self.customer_quotation_code.strip()

        if not self.customer_code:
            raise ValueError("customer_code is required.")
        if not self.shop_code:
            raise ValueError("shop_code is required.")
        if not self.items:
            raise ValueError("At least one item is required.")