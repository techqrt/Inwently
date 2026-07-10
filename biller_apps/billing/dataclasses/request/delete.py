from dataclasses import dataclass


@dataclass
class BillingDeleteRequest:
    bill_number: str
