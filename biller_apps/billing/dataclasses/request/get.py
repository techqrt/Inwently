from biller_apps.common.dataclasses.get import Get


class BillingGetRequest(Get):
    bill_number: str
