from dataclasses import dataclass

@dataclass
class POSRequest:
    billed_by: str
    customer_id: int
    item_id: int
    quantity: float
    price: float
    tax: float
    discount: float
    total: float
    shop_code: str