from dataclasses import dataclass

from biller_apps.common.dataclasses.get_all import GetAll


@dataclass
class ShopGetAll(GetAll):
    type: str
