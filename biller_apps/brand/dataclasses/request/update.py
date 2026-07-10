from dataclasses import dataclass


@dataclass
class BrandUpdateRequest:
    brand_code: str
    name: str
