from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class StockTransferGet(Get):
    transfer_code: str
