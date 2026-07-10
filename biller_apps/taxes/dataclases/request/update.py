from dataclasses import dataclass


@dataclass
class TaxesUpdate:
    tax_code: str
    name: str
    total_tax: float
    tax_splits: dict
