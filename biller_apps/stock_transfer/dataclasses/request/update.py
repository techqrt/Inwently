from dataclasses import dataclass
from datetime import datetime

@dataclass
class StockTransferUpdate:
    source_shop_id: int
    destination_shop_id: int
    item_id: int
    quantity: int
    transfer_date_time: datetime
    status: str
    organisation_id: int
    remarks: str 
    requested_by: str 
    approved_by: str
