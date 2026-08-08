from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class InventoryCreate:
    item_code: str
    shop_code: str
    expiry_date: Optional[date]
    price: Decimal
    balance_qty: int
    store_mapping: str = ""

    def __post_init__(self):
        self.item_code = self.item_code.strip()
        self.shop_code = self.shop_code.strip()
        self.store_mapping = self.store_mapping.strip()

        if not self.item_code:
            raise ValueError("item_code is required.")

        if not self.shop_code:
            raise ValueError("shop_code is required.")

        if self.balance_qty < 0:
            raise ValueError("balance_qty cannot be negative.")

        if self.price < 0:
            raise ValueError("price cannot be negative.")