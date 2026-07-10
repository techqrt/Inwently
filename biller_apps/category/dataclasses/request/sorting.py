from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryListRequest:
    sort_order: Optional[str]
