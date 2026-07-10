from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class ItemGet(Get):
    item_code: str
