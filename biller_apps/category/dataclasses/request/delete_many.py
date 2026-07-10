from dataclasses import dataclass


@dataclass
class CategoryDeleteManyRequest:
    category_code: list
