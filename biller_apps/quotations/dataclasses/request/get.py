from dataclasses import dataclass

from biller_apps.common.dataclasses.get import Get


@dataclass
class QuotationGet(Get):
    quotation_code: str
