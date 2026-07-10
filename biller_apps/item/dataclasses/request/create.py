import datetime
from dataclasses import dataclass


@dataclass
class ItemRequest:
    name: str
    description: str
    bar_qr_code: str
    brand_code: str
    category_code: str
    supplier_code: str
    image_url: str
    tax_code: int
    hsn_code: str
