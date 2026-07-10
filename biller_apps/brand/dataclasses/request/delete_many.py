from dataclasses import dataclass


@dataclass
class BrandDeleteManyRequest:
    brand_code: list
