import datetime
from dataclasses import dataclass


@dataclass
class CustomerUpdateRequest:
    name: str
    customer_code: str
    state: str
    country: str
    street: str
    mobile_number: str
    email_id: str
    id_number: str
    id_type: str
    photo_url: str
    id_proof_url: str
    occupation: str
    date_of_birth: datetime.datetime
    gender: str
    martial_status: str
    religion: str
    blood_group: str
    education: str
