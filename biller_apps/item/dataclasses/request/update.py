from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemUpdate:
    name: str
    item_code: str
    description: str
    bar_qr_code: str
    brand_code: str
    category_code: str
    supplier_code: str
    image_url: str
    tax_code: str
    hsn_code: str
    no_of_packets: int = 1
    sku_code: str = ''
    plain_price: float = 0.00
    printed_price: float = 0.00
    moq: float = 1.00
    # None = not sent by the client -> leave existing attributes/images untouched.
    # [] (explicit empty list) = client wants them cleared.
    attributes: Optional[list] = None
    other_images: Optional[list] = None