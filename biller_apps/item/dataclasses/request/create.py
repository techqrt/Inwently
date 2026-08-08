import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ItemRequest:
    name: str
    description: str
    bar_qr_code: str
    brand_code: str
    category_code: str
    supplier_code: str
    image_url: str
    tax_code: Optional[int]
    hsn_code: str
    no_of_packets: int = 1
    sku_code: str = ''
    plain_price: float = 0.00
    printed_price: float = 0.00
    moq: float = 1.00
    attributes: list = field(default_factory=list)
    other_images: list = field(default_factory=list)
    # Only used by the CSV bulk-upload path (parse_csv / bulk_create_extract)
    bar_qr_auto: bool = False
    created_time: Optional[datetime.datetime] = None

