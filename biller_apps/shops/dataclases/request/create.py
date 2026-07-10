from dataclasses import dataclass


@dataclass
class ShopsRequest:
    name: str
    state: str
    country: str
    street: str
    type: str
    email_id: str
    mobile_number: str
    alt_mobile_number: str
    website: str
