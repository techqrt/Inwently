from dataclasses import dataclass


@dataclass
class ShopsUpdateRequest:
    name: str
    state: str
    country: str
    street: str
    email_id: str
    mobile_number: str
    alt_mobile_number:str
    website: str
    shop_code: str
    type: str
