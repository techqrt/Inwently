from dataclasses import dataclass


@dataclass
class BillingRequest:
    billed_by: str
    shop_code: str
    items: list
