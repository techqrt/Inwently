from dataclasses import dataclass


@dataclass
class CategoryDeleteRequest:
    category_code: str
