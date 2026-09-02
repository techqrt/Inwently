# biller_apps/pos/dataclasses/request/dispatch_details.py
from dataclasses import dataclass


@dataclass
class POSDispatchDetails:
    pos_id: int
    logistics_company: str
    logistics_charges: float
