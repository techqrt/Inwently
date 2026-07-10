from dataclasses import dataclass


@dataclass
class ReturnItemRequest:
    purchase_bill_number: str
    supplier_code: str
    item_code: str
    return_reason: str
    quantity: float
    price: float
    tax: float
