# biller_apps/pos/dataclasses/request/update.py
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


@dataclass
class POSItemAddEntry:
    item_code: str
    quantity: int
    price: Decimal
    tax: Decimal = Decimal("0")
    discount: Decimal = Decimal("0")

    def __post_init__(self):
        self.item_code = self.item_code.strip()
        if not self.item_code:
            raise ValueError("item_code is required.")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive.")
        if self.price < 0 or self.tax < 0 or self.discount < 0:
            raise ValueError("price, tax and discount cannot be negative.")


@dataclass
class POSItemUpdateEntry:
    pos_item_id: int
    quantity: Optional[int] = None
    price: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    discount: Optional[Decimal] = None


@dataclass
class POSUpdate:
    pos_id: int
    items_to_add: list = field(default_factory=list)       # list[POSItemAddEntry]
    items_to_update: list = field(default_factory=list)    # list[POSItemUpdateEntry]
    items_to_remove: list = field(default_factory=list)    # list[int] (pos_item_id)
    discounts: Optional[Decimal] = None
    discounts_unit: Optional[str] = None
    wave_off: Optional[Decimal] = None
    payment_type: Optional[str] = None

    def __post_init__(self):
        if not (self.items_to_add or self.items_to_update or self.items_to_remove
                or self.discounts is not None or self.discounts_unit is not None
                or self.wave_off is not None or self.payment_type is not None):
            raise ValueError("At least one change (item or header field) is required.")