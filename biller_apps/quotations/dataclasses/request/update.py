from dataclasses import dataclass

@dataclass
class QuotationUpdate:
    supplier_id: int
    organisation_id: int
    item_id: int
    quotation_code:int
    description: str
    brand: str
    quantity: float
    price: float
    tax: float
    total: float
    purchase: bool
    sales: bool
