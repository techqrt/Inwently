from dataclasses import dataclass
from datetime import datetime

@dataclass
class StockTransferRequest:
    source_shop_code: str
    destination_shop_code: str
    item_code: str
    quantity: int
    transfer_date_time: datetime
    status: str
    remarks: str 
    requested_by: str 
    approved_by: str
