from dataclasses import dataclass


@dataclass
class SupplierDeleteManyRequest:
    supplier_code: list
