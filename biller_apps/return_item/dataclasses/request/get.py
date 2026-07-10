from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class ReturnItemGet(Get):
    return_code: str
