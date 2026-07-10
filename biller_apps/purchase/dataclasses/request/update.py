from dataclasses import dataclass


@dataclass
class PurchaseUpdate:
    purchase_bill_number: str
    supplier_code: str
    item_code: str
    buying_price: float
    landing_cost: float
    selling_price: float
    tax: float
    quantity: float
    bill_amount: float
    purchase_code: str
