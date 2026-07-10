from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class ShopGet(Get):
    shop_code: str
