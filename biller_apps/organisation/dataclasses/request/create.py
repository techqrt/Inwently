from dataclasses import dataclass, field
from datetime import date

@dataclass
class OrganisationRequest:
    owner_name: str
    owner_mobile: str
    owner_alternate_mobile: str
    name: str
    state: str
    country: str
    street: str
    shop_count: int
    employee_count: int
    plan: str
    plan_expiry: date
    owner_email: str
    approval: bool = field(default=False)
