from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class ReturnPurchaseGet(Get):
    return_code: str
