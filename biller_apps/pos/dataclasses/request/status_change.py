# biller_apps/pos/dataclasses/request/status_change.py
from dataclasses import dataclass


@dataclass
class POSStatusChange:
    pos_id: int