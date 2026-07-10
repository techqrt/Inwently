from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class SuppliersGet(Get):
    supplier_code: str
