from dataclasses import dataclass


@dataclass
class SupplierUpdate:
    name: str
    state: str
    country: str
    street: str
    mobile_number: str
    email_id: str
    alt_mobile_number: str
    id_number: str
    id_type: str
    gst_number: str
    photo_url: str
    id_proof_url: str
    supplier_code: str
