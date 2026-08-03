from dataclasses import dataclass

@dataclass
class InventoryGetAll:
    values: str
    page_num: int
    limit: int
    sort_by: str
    sort_order: str
    filter_key: str
    filter_value: str
    shop_code: str
    item_code: str

    def __post_init__(self):
        self.values_list = self.values.split(',') if self.values and len(self.values.split(',')) > 0 else []
        field_mappings = {
            "name": "item_id__name",
            "item_name": "item_id__name",
            "branch_name": "shop_id__name"
        }

        self.sort_by = field_mappings.get(self.sort_by, self.sort_by)  # Convert if in mappings

        if not self.sort_by:
            self.sort_by = "item_id__name"

        if not self.sort_order:
            self.sort_order = "asc"

        self.ordering = f"{'-' if self.sort_order == 'desc' else ''}{self.sort_by}"
