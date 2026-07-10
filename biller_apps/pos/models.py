from django.db import models
from django.utils import timezone

from biller_apps.billing.models.customer_bills import CustomerBills
from biller_apps.customer.models import Customer
from biller_apps.organisation.models import Organisation
from biller_apps.item.models.items import Items



class POS(models.Model):
    pos_id = models.AutoField(primary_key=True)
    payment_type = models.CharField(max_length=15, default='', unique=True)
    customer_billing = models.ForeignKey(CustomerBills, on_delete=models.CASCADE,default=None,null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'pos'

    @staticmethod
    def calculate_total_price(price: float, tax: float, discount: float, quantity: float) -> float:
        subtotal = (price + tax) * quantity
        return subtotal - discount

    def create(self, customer_id: int, organisation_id: int, organisation_name: str, item_id: int,
               quantity: float, price: float, tax: float, discount: float, payment_status: str, payment_method: str) -> int:
        self.customer = Customer(customer_id)
        self.organisation = Organisation(organisation_id)
        self.item = Items(item_id)
        self.quantity = quantity
        self.price = price
        self.tax = tax
        self.discount = discount
        self.total = self.calculate_total_price(price, tax, discount, quantity)
        self.created_date = timezone.now()
        self.save()
        self.pos_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(self.pos_id)
        self.save()
        return self.pos_id