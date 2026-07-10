from dataclasses import dataclass


@dataclass
class ItemDeleteManyRequest:
    item_code: list
