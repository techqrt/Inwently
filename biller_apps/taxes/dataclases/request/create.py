from dataclasses import dataclass


@dataclass
class TaxesCreate:
    name: str
    total_tax: float
    tax_splits: dict
