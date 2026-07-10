from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class PurchaseGet(Get):
    purchase_code: str
