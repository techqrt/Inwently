from dataclasses import dataclass


@dataclass
class CategoryUpdateRequest:
    category_code: str
    name: str
