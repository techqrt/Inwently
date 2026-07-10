import uuid
from datetime import datetime

from django.db import models
from django.db.models import Sum
from django.utils import timezone

from biller_apps.billing.models.customer_bills import CustomerBills
from biller_apps.item.models.items import Items



class Billing(models.Model):
    billing_id = models.AutoField(primary_key=True)
    customer_billing_id = models.ForeignKey(CustomerBills,on_delete=models.CASCADE,default=None,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    item_id = models.ForeignKey(Items, on_delete=models.DO_NOTHING)
    quantity = models.FloatField(default=0)
    total_price = models.FloatField(default=0)


    class Meta:
        db_table = 'billing'

    @staticmethod
    def get_sum_annotation(item_id: list, organisation_name: str) -> list:
        return Billing.objects.filter(item_id__in=item_id, organisation_id__company_name=organisation_name).values(
            'shop_id', 'item_id').annotate(total_expense=Sum('quantity'))

    def create(self, created_at: datetime, item_id: int, quantity: float, mrp_price: float,customer_billing_id:int) -> int:
        self.created_at = created_at
        self.customer_billing_id = CustomerBills.objects.get(customer_billing_id=customer_billing_id)
        self.item_id = Items.objects.get(item_id=item_id)
        self.quantity = quantity
        self.total_price = quantity * mrp_price
        self.save()
        return self.billing_id

    @staticmethod
    def get_annotate_sum_total_price(organisation_name: str):
        return Billing.objects.filter(customer_billing_id__organisation_id__company_name=organisation_name).values(
            'created_at', bill_number=models.F('customer_billing_id__bill_number')
        ).annotate(total_price=Sum('total_price')).order_by('bill_number', 'created_at')

    @staticmethod
    def get(organisation_name: str, bill_number: str):
        return Billing.objects.filter(customer_billing_id__organisation_id__company_name=organisation_name,
                                      customer_billing_id__bill_number=bill_number).values(
            'quantity', 'total_price', 'item_id__name', 'customer_billing_id__billed_by__employee_code',
            'customer_billing_id__shop_id__shop_code')

    @staticmethod
    def remove(organisation_name: str, bill_number: str):
        Billing.objects.filter(customer_billing_id__organisation_id__company_name=organisation_name,
                               customer_billing_id__bill_number=bill_number).delete()
