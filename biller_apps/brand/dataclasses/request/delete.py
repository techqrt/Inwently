from dataclasses import dataclass


@dataclass
class BrandDeleteRequest:
    brand_code: str
