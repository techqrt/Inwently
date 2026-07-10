from dataclasses import dataclass


@dataclass
class ReturnPurchaseRequest:
    purchase_id: int
    supplier_id: int
    organisation_id: int
    item_id: int
    return_reason: str
    quantity: float
    tax: float
    total_price: float
