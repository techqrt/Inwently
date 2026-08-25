from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class BillingGetRequest(Get):
    bill_number: str
