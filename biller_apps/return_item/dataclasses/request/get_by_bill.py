from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class ReturnItemGetByBill(Get):
    bill_number: int
