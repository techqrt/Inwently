from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class CustomerGet(Get):
    customer_code: str
