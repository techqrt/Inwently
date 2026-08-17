# biller_apps/pos/dataclasses/request/get.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class POSGet:
    pos_id: Optional[int] = None
    pos_code: Optional[str] = None

    def __post_init__(self):
        if not self.pos_id and not self.pos_code:
            raise ValueError("Either pos_id or pos_code is required.")