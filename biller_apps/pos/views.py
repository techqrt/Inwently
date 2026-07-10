import json
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone

from biller.constants import Constants
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.billing.models.billing import Billing
from biller_apps.common.common import Common
from biller_apps.common.utils import Utils
from biller_apps.pos.dataclasses.request.create import POSRequest
from biller_apps.pos.models import POS
from biller_apps.customer.models import Customer
from biller_apps.employees.models.employees import Employees
from biller_apps.item.models.items import Items

from biller_apps.shops.models import Shops

class POSView:
    def __init__(self):
        self.data_created = "POS transaction added successfully"
        super().__init__()
    
    @Common().exception_handler
    def create_extract(self, params: list[POSRequest], token_payload: Payload):
        created_transactions = []

        with transaction.atomic():
            for param in params:
                employee = Employees.get_by_email(email=param.billed_by,
                                          organisation_name=token_payload.organisationName)
                shop = Shops.objects.filter(shop_code=param.shop_code).values('shop_id').first()
                customer_exists = Customer.objects.filter(customer_id=param.customer_id).exists()
                item_exists = Items.objects.filter(item_id=param.item_id).exists()

                if not customer_exists:
                    raise ValueError(Constants.customer_not_found)
                if not item_exists:
                    raise ValueError(Constants.item_not_found)

                total_price = POS.calculate_total_price(
                    price=param.price, tax=param.tax, discount=param.discount, quantity=param.quantity
                )
                created_at = timezone.now()
                billing = Billing().create(created_at=created_at,
                                 employee_id=employee['employee_id'], item_id=param.item_id,
                                 organisation_id=token_payload.organisation_id, shop_id=shop['shop_id'],
                                 quantity=param.quantity, mrp_price=param.price)
                billing_extract = Billing.objects.get(billing_id=billing)
                pos = POS().create(
                    customer_id=param.customer_id,
                    organisation_id=token_payload.organisation_id,
                    organisation_name=token_payload.organisationName,
                    item_id=param.item_id,
                    quantity=param.quantity,
                    price=param.price,
                    tax=param.tax,
                    discount=param.discount,
                )
                pos_extract = POS.objects.get(pos_id=pos)
                created_transactions.append({
                    "billing_id": billing,
                    "billing_number": billing_extract.bill_number,
                    "billing_created_at": billing_extract.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "pos_id": pos_extract.pos_id,
                    "customer_id": pos_extract.customer,
                    "item_id": pos_extract.item,
                    "quantity": pos_extract.quantity,
                    "price": pos_extract.price,
                    "tax": pos_extract.tax,
                    "discount": pos_extract.discount,
                    "total": pos_extract.total
                })
        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.data_created))
