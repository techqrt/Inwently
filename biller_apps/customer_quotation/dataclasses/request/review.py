# biller_apps/customer_quotation/dataclasses/request/review.py
from dataclasses import dataclass


@dataclass
class CustomerQuotationReview:
    customer_quotation_id: int
    status: str  # 'phone_confirmed' or 'rejected' or 'cancelled'

    def __post_init__(self):
        allowed = {"phone_confirmed", "rejected", "cancelled"}
        if self.status not in allowed:
            raise ValueError(f"status must be one of: {', '.join(sorted(allowed))}")