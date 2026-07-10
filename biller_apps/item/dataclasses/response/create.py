from dataclasses import dataclass


@dataclass
class ItemCreateResponse:
    itemCode: str
    code: str
