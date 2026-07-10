from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class BranchSplitDataclass:
    branch_code: str
    quantity: float

@dataclass
class PurchaseItemsDataclass:
    item_code: str
    buying_price: float
    selling_price: float
    expiry: datetime
    tax: float = 0.0
    quantity: float = 1.0
    landing_cost: float = 0.0
    unit: str = "Kg"
    branch_split: List[BranchSplitDataclass] = field(default_factory=list)

@dataclass
class PurchaseRequestDataclass :
    purchase_bill_number: str
    supplier_code: str
    items: List[PurchaseItemsDataclass]
    bill_amount: float

    def __post_init__(self):
        # Calculate total buying price
        total_buying_price = sum(item['buying_price'] + item['tax'] for item in self.items)

        # Validate if total buying price matches bill amount
        if total_buying_price != self.bill_amount:
            raise ValueError(
                f"Total buying price ({total_buying_price}) does not match bill_amount ({self.bill_amount})"
            )
