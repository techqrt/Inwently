from django.db import models
from django.db.models import Q
from django.utils import timezone
from biller_apps.billing.models.billing import Billing
from biller_apps.billing.models import Billing
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.supplier.models import Supplier
from biller_apps.organisation.models import Organisation
from biller_apps.item.models.items import Items


class ReturnItem(models.Model):
    return_id = models.AutoField(primary_key=True)
    return_code = models.CharField(max_length=10, default='', unique=True)
    bill = models.ForeignKey(Billing, on_delete=models.CASCADE, related_name='return_items')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    return_reason = models.TextField(default='', null=True, blank=True)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'return_item'

    def create(self, bill_id: int, supplier_id: int, organisation_id: int, item_id: int,
               organisation_name: str, return_reason: str, quantity: float, price: float, tax: float) -> int:
        self.bill = Billing(bill_id)
        self.supplier = Supplier(supplier_id)
        self.organisation_id = Organisation(organisation_id)
        self.item = Items(item_id)
        self.return_reason = return_reason
        self.quantity = quantity
        self.price = price
        self.tax = tax
        self.total_price = self.calculate_total_price(quantity, price, tax)
        self.created_date_time = timezone.now()
        self.save()
        self.return_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(self.return_id)
        self.save()
        return self.return_id

    @staticmethod
    def get(return_code: str, organisation_name: str) -> dict:
        return ReturnItem.objects.filter(
            return_code=return_code, organisation_id__company_name=organisation_name
        ).values(
            'return_id', 'supplier__name', 'item__name',
            'return_reason', 'quantity', 'price', 'tax', 'total_price', 'created_date_time'
        ).first()

    @staticmethod
    def get_all(organisation_name: str,params:GetAll) -> list:
        filters=Q(organisation_id__company_name=organisation_name)
        if params.filter_key and params.filter_value:
            if params.filter_value=='is_active':
                filters&=Q(**{params.filter_key:params.filter_value.lower()=='true'})
            else:
                filters&=Q(**{params.filter_key:params.filter_value})
        if len(params.search_key)>0:
            filters&=Q(return_code__icontains=params.search_key)
        if params.sort_by == 'name':
            params.sort_by = "created_date_time"
            params.sort_order = 'desc'
            params.ordering = f"{'-' if params.sort_order == 'desc' else ''}{params.sort_by}"
        return ReturnItem.objects.filter(filters).values(
            'return_code', 'bill__customer_billing_id__bill_number', 'supplier__name', 'created_date_time', 'total_price'
        ).order_by(params.ordering)

    @staticmethod
    def update(return_id: int, return_reason: str, quantity: float, price: float, tax: float) -> int:
        return_item = ReturnItem.objects.get(return_id=return_id)
        return_item.return_reason = return_reason
        return_item.quantity = quantity
        return_item.price = price
        return_item.tax = tax
        return_item.total_price = return_item.calculate_total_price(quantity, price, tax)
        return_item.save()
        return return_item.return_id

    @staticmethod
    def calculate_total_price(quantity: float, price: float, tax: float) -> float:
        return (quantity * price) + tax

    @staticmethod
    def remove(return_id: int):
        ReturnItem.objects.get(return_id=return_id).delete()

    @staticmethod
    def get_item_by_bill(bill_number: int, organisation_name: str) -> list:
        return Billing.objects.filter(
            bill_number=bill_number, organisation_id__company_name=organisation_name
        ).values(
            'item_id__item_code', 'item_id__name', 'quantity', 'total_price'
        ).order_by('-created_at')