from dataclasses import dataclass


@dataclass
class BillingRequest:
    customer_name: str
    customer_phone: str
    billed_by: str
    shop_code: str
    items: list  # list[POSItemAddEntry]

    def __post_init__(self):
        self.customer_name = self.customer_name.strip()
        self.customer_phone = self.customer_phone.strip()
        if not self.customer_name:
            raise ValueError("customer_name is required.")
        if not self.customer_phone:
            raise ValueError("customer_phone is required.")
        if not self.items:
            raise ValueError("At least one item is required.")
