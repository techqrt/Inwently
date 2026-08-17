# biller_apps/customer_quotation/dataclasses/request/get.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class CustomerQuotationGet:
    customer_quotation_id: Optional[int] = None
    customer_quotation_code: Optional[str] = None

    # def __post_init__(self):
    #     if not self.customer_quotation_id and not self.customer_quotation_code:
    #         raise ValueError("Either customer_quotation_id or customer_quotation_code is required.")