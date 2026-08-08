from dataclasses import dataclass
from typing import Optional


@dataclass
class InventoryGet:
    inventory_id: Optional[int] = None
    inventory_code: Optional[str] = None

    def __post_init__(self):
        if not self.inventory_id and not self.inventory_code:
            raise ValueError("Either inventory_id or inventory_code is required.")

        if self.inventory_code is not None:
            self.inventory_code = self.inventory_code.strip()