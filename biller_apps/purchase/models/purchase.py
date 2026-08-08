import urllib
from datetime import datetime

from django.db import models
from django.db.models import Q
from django.utils import timezone

from biller_apps.purchase.models.purchase_bills import PurchaseBills
from biller_apps.billing.models import Billing
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.supplier.models import Supplier
from biller_apps.item.models.items import Items



class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    purchase_bill = models.ForeignKey(PurchaseBills,on_delete=models.CASCADE,default=None)
    item = models.ForeignKey(Items, on_delete=models.DO_NOTHING)
    buying_price = models.FloatField(default=0)
    landing_cost = models.FloatField(default=0)
    selling_price = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    quantity_unit = models.CharField(max_length=10, default='Kg')
    expiry = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'purchase'

    def create(self, purchase_bill: str,item_id: str, buying_price: float,
              landing_cost: float, selling_price: float, tax: float, quantity: str, quantity_unit: float,expiry:datetime) -> int:
        self.purchase_bill = PurchaseBills(purchase_bill_id=purchase_bill)
        self.item = Items.objects.filter(item_code=item_id).first()
        self.buying_price = buying_price
        self.landing_cost = landing_cost
        self.selling_price = selling_price
        self.tax = tax
        self.quantity = quantity
        self.expiry = expiry
        self.save()
        return self.purchase_id

    @staticmethod
    def get(purchase_code: str, organisation_name: str) -> dict:
        return Purchase.objects.filter(purchase_bill__purchase_code=purchase_code,
                                       purchase_bill__organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
            'purchase_id', 'purchase_bill__supplier__name', 'item__name',
            'buying_price', 'landing_cost', 'selling_price', 'tax', 'quantity', 'purchase_bill__created_date_time'
        ).first()

    @staticmethod
    def get_all(organisation_name: str,params:GetAll) -> list:
        filters=Q(purchase_bill__organisation_id__company_name=organisation_name)

        if params.filter_value and params.filter_key:
            if params.filter_key.lower() == 'is_active':
                filters &= Q(is_active=params.filter_value.lower() == 'true')
            else:
                filters &= Q(**{params.filter_key: params.filter_value})

            if len(params.search_key) > 0:
                filters=filters & (Q(purchase_bill__purchase_bill_number__icontains=params.search_key)|Q(purchase_bill__supplier__name__icontains=params.search_key))
        if params.sort_by == 'name':
            params.sort_by = "purchase_bill_number"
        params.ordering = f"{'-' if params.sort_order == 'desc' else ''}purchase_bill__{params.sort_by}"
        return Purchase.objects.filter(filters).values(
            'purchase_bill__purchase_bill_number', 'purchase_bill__supplier__name',
            'purchase_bill__created_date_time', 'purchase_bill__bill_amount', 'purchase_bill__purchase_code'
        ).order_by(params.ordering)

    @staticmethod
    def update(purchase_id: int, buying_price: float, landing_cost: float, selling_price: float,
               tax: float, quantity: float, bill_amount: float,) -> int:
        purchase = Purchase.objects.get(purchase_id=purchase_id)
        purchase.buying_price = buying_price
        purchase.landing_cost = landing_cost
        purchase.selling_price = selling_price
        purchase.tax = tax
        purchase.quantity = quantity
        purchase.bill_amount = bill_amount
        purchase.save()
        return purchase.purchase_id
    
    @staticmethod
    def total_price(self) -> float:
        return (self.buying_price * self.quantity) + self.tax
    
    @staticmethod
    def remove(purchase_id: int):
        Purchase.objects.get(purchase_id=purchase_id).delete()