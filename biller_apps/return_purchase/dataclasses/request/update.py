from dataclasses import dataclass


@dataclass
class ReturnPurchaseUpdate:
    purchase_id: int
    supplier_id: int
    organisation_id: int
    item_id: int
    return_reason: str
    quantity: float
    tax: float
    total_price: float
    return_code: str
