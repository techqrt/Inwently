from dataclasses import dataclass
from typing import Optional


@dataclass
class BrandListRequest:
    sort_order: Optional[str]
