import uuid

from django.db import models
from django.db.models import Q

from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.organisation.models import Organisation


class Taxes(models.Model):
    tax_id = models.AutoField(primary_key=True)
    tax_code = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    total_tax = models.FloatField(default=0.0)
    tax_splits = models.JSONField(default=dict)
    secure = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'taxes'

    def create(self, name: str, total_tax: float, tax_splits: dict, organisation_id: int, organisation_name: str,
               secure: bool = False) -> int:
        self.name = name
        self.total_tax = total_tax
        self.tax_splits = tax_splits
        self.organisation_id = Organisation(organisation_id)
        self.secure = secure
        if secure:
            code_id = str(uuid.uuid4())[-8:]
        else:
            self.save()
            code_id = self.tax_id
        self.tax_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(code_id)
        self.save()
        return self.tax_id

    @staticmethod
    def get_all(organisation_name: str,params:GetAll) -> list:
        filters= Q(organisation_id__company_name=organisation_name)
        if params.filter_key and params.filter_value:
            if params.filter_key.lower() == 'is_active':
                filters &= Q(is_active=params.filter_value.lower() == 'true')
            else:
                filters &= Q(**{params.filter_key:params.filter_value})
        if len(params.search_key)>0:
            filters &= Q(name__icontains=params.search_key)
        return Taxes.objects.filter(filters).values(
            'name', 'total_tax', 'tax_splits', 'tax_code').order_by(params.ordering)

    @staticmethod
    def update(tax_id: int, name: str, total_tax: float, tax_splits: dict) -> int:
        tax = Taxes.objects.get(tax_id=tax_id)
        tax.name = name
        tax.total_tax = total_tax
        tax.tax_splits = tax_splits
        tax.save()
        return tax.tax_id

    @staticmethod
    
    def get(organisation_name: str, tax_code: str):
        
        return Taxes.objects.filter(organisation_id__company_name=organisation_name, tax_code=tax_code).values().first()

    @staticmethod
    def get_from_list(organisation_name: str, tax_codes: list):
        return Taxes.objects.filter(organisation_id__company_name=organisation_name, tax_code__in=tax_codes).values()

    @staticmethod
    def delete_many(organisation_name: str, tax_codes: list):
        return Taxes.objects.filter(organisation_id__company_name=organisation_name, tax_code__in=tax_codes).delete()

    @staticmethod
    def get_sorted_taxes(organisation_name: str, sort_order: str) -> list:
        order_by = 'name' if sort_order == 'asc' else '-name'
        return Taxes.objects.filter(organisation_id__company_name=organisation_name).values('name', 'tax_code',
                                                                                    'total_tax').order_by(order_by)
