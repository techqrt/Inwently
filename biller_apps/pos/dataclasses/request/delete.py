# biller_apps/pos/dataclasses/request/delete.py
from dataclasses import dataclass


@dataclass
class POSDelete:
    pos_id: int
    pos_code: str