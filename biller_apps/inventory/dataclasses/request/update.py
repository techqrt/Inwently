from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass
class InventoryUpdate:
    inventory_id: int
    item_code: Optional[str] = None
    shop_code: Optional[str] = None
    expiry_date: Optional[date] = None
    price: Optional[Decimal] = None
    balance_qty: Optional[int] = None
    store_mapping: Optional[str] = None

    def __post_init__(self):
        if self.item_code is not None:
            self.item_code = self.item_code.strip()

            if not self.item_code:
                raise ValueError("item_code cannot be blank.")

        if self.shop_code is not None:
            self.shop_code = self.shop_code.strip()

            if not self.shop_code:
                raise ValueError("shop_code cannot be blank.")

        if self.price is not None and self.price < 0:
            raise ValueError("price cannot be negative.")

        if self.balance_qty is not None and self.balance_qty < 0:
            raise ValueError("balance_qty cannot be negative.")

        if self.store_mapping is not None:
            self.store_mapping = self.store_mapping.strip()