from dataclasses import dataclass
from datetime import datetime
from biller_apps.common.dataclasses.get import Get

@dataclass
class OverviewReportItemGet:
    page_num: int
    limit: int
    start_date: datetime
    end_date: datetime
    sort_by: str
    sort_order: str
    filter_key: str
    filter_value: str

    def __post_init__(self):
        self.values_list = []
        
        field_mappings = {
            "item_name": "item_id__name"
        }

        self.sort_by = field_mappings.get(self.sort_by, self.sort_by)  # Convert if in mappings

        if not self.sort_by:
            self.sort_by = "item_id__name"

        if not self.sort_order:
            self.sort_order = "asc"

        self.ordering = f"{'-' if self.sort_order == 'desc' else ''}{self.sort_by}"
