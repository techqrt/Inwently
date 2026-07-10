from dataclasses import dataclass


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
