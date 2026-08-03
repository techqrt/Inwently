from dataclasses import dataclass
from datetime import datetime
from biller_apps.common.dataclasses.get import Get

@dataclass
class GeneralReportGet:
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
        # Filter/Sort keys coming from Swagger
        "name": "item__name",
        "item_name": "item__name",
        "supplier_name": "purchase_bill__supplier__name",
        "price": "buying_price",
        "qty": "quantity",
        "bill_amount": "purchase_bill__bill_amount",
        "bill_number": "purchase_bill__purchase_bill_number",
        "purchase_code": "purchase_bill__purchase_code",
        "date": "purchase_bill__created_date_time",}

        if self.sort_by:
         self.sort_by = field_mappings.get(self.sort_by, self.sort_by)
        else:
         self.sort_by = "purchase_bill__created_date_time"

        if self.filter_key:
         self.filter_key = field_mappings.get(self.filter_key, self.filter_key)


        

        if not self.sort_order:
         self.sort_order = "asc"

        self.ordering = f"{'-' if self.sort_order == 'desc' else ''}{self.sort_by}"