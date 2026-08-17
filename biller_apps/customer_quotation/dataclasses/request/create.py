# biller_apps/customer_quotation/dataclasses/request/create.py
from dataclasses import dataclass


@dataclass
class CustomerQuotationItemCreate:
    item_code: str
    quantity: int

    def __post_init__(self):
        self.item_code = self.item_code.strip()
        if not self.item_code:
            raise ValueError("item_code is required.")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive.")


@dataclass
class CustomerQuotationCreate:
    customer_name: str
    customer_phone: str
    shop_code: str
    items: list  # list[CustomerQuotationItemCreate]
    customer_email: str = ""

    def __post_init__(self):
        self.customer_name = self.customer_name.strip()
        self.customer_phone = self.customer_phone.strip()
        self.shop_code = self.shop_code.strip()

        if not self.customer_name:
            raise ValueError("customer_name is required.")
        if not self.customer_phone:
            raise ValueError("customer_phone is required.")
        if not self.shop_code:
            raise ValueError("shop_code is required.")
        if not self.items:
            raise ValueError("At least one item is required.")