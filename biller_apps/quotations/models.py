from django.db import models
from django.db.models import Q
from django.utils import timezone
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.supplier.models import Supplier
from biller_apps.organisation.models import Organisation
from biller_apps.item.models.items import Items


class Quotation(models.Model):
    quotation_id = models.AutoField(primary_key=True)
    quotation_code = models.CharField(max_length=15, default='', unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    total_amount = models.FloatField(default=0)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    description = models.TextField(default='', null=True, blank=True)
    brand = models.CharField(max_length=100, default='')
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    total = models.FloatField(default=0)
    purchase = models.BooleanField(default=False)
    sales = models.BooleanField(default=False)

    class Meta:
        db_table = 'quotation'

    @staticmethod
    def calculate_total_price(price: float, tax: float, quantity: float) -> float:
        return (price + tax) * quantity

    def create(self, supplier_id: int, organisation_id: int, organisation_name: str, item_id: int,
               description: str, brand: str, quantity: float, price: float, tax: float, purchase: bool, sales: bool) -> int:
        self.supplier = Supplier(supplier_id)
        self.organisation_id = Organisation(organisation_id)
        self.item = Items(item_id)
        self.description = description
        self.brand = brand
        self.quantity = quantity
        self.price = price
        self.tax = tax
        self.total = self.calculate_total_price(price, tax, quantity)
        self.purchase = purchase
        self.sales = sales
        self.created_date = timezone.now()
        self.save()
        self.quotation_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(self.quotation_id)
        self.save()
        return self.quotation_id

    @staticmethod
    def get(quotation_code: str, organisation_name: str) -> dict:
        return Quotation.objects.filter(quotation_code=quotation_code, organisation_id__company_name=organisation_name).values(
            'quotation_id', 'supplier__name', 'item__name', 'description', 'brand', 'quantity', 'price', 'tax', 'total', 'purchase', 'sales', 'total_amount', 'created_date'
        ).first()

    @staticmethod
    def get_all(organisation_name: str,params:GetAll) -> list:
        filters= Q(organisation_id__company_name=organisation_name)
        if params.filter_key and params.filter_value:
            if params.filter_value=='is_active':
                filters=filters & Q(**{params.filter_key:params.filter_value.lower()=='true'})
            else:
                filters=filters & Q(**{params.filter_key:params.filter_value})
        if len(params.search_key)>0:
            filters=filters & Q(quotation_code__icontains=params.search_key)
        if params.sort_by == 'name':
            params.sort_by = "created_date"
            params.ordering = f"{'-' if params.sort_order == 'desc' else ''}{params.sort_by}"
        return Quotation.objects.filter(filters).values(
            'quotation_id', 'quotation_code', 'sales', 'purchase', 'supplier__name', 'quantity', 'total'
        ).order_by(params.ordering)

    @staticmethod
    def update(quotation_id: int, description: str, brand: str, quantity: float, price: float, tax: float, purchase: bool, sales: bool) -> int:
        quotation = Quotation.objects.get(quotation_id=quotation_id)
        quotation.description = description
        quotation.brand = brand
        quotation.quantity = quantity
        quotation.price = price
        quotation.tax = tax
        quotation.total = Quotation.calculate_total_price(price, tax, quantity)
        quotation.purchase = purchase
        quotation.sales = sales
        quotation.save()
        return quotation.quotation_id

    @staticmethod
    def remove(quotation_id: int):
        Quotation.objects.get(quotation_id=quotation_id).delete()


