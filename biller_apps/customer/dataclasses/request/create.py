from dataclasses import dataclass


@dataclass
class CustomerRequest:
    name: str
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
    date_of_birth: str
    gender: str
    martial_status: str
    religion: str
    blood_group: str
    education: str
