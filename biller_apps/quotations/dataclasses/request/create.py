from dataclasses import dataclass

@dataclass
class QuotationRequest:
    supplier_id: int
    organisation_id: int
    item_id: int
    description: str
    brand: str
    quantity: float
    price: float
    tax: float
    total: float
    purchase: bool
    sales: bool
