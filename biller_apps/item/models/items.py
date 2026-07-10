import datetime
import urllib

from django.db import models
from django.db.models import Q
from django.utils import timezone

from biller_apps.brand.models import Brand
from biller_apps.category.models import Category
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.organisation.models import Organisation
from biller_apps.supplier.models import Supplier
from biller_apps.taxes.models import Taxes


class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='', unique=True)
    description = models.CharField(max_length=350, default='')
    code = models.CharField(max_length=100, default='', unique=True)
    hsn_code = models.CharField(max_length=100, default='')
    tax_code = models.ForeignKey(Taxes, on_delete=models.DO_NOTHING, default=1)
    is_active = models.BooleanField(default=False)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING)
    item_code = models.CharField(max_length=10, default='', unique=True)
    brand_id = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, default=1)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, default=1)
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default=1)
    created_time = models.DateTimeField(default=timezone.now)
    image_url = models.TextField(default='', null=True)

    class Meta:
        db_table = 'items'

    def create(self, name: str, description: str, organisation_name: str,
               bar_qr_code: str, organisation_id: int, brand_id: int, category_id: int, supplier_id: int,
               image_url: str,hsn_code:str,tax_id:int):
        self.name = name
        self.description = description if description is not None else ''
        self.is_active = True
        self.organisation_id = Organisation.objects.get(organisation_id=organisation_id)
        self.brand_id = Brand.objects.get(brand_id=brand_id)
        self.category_id = Category.objects.get(category_id=category_id)
        self.supplier_id = Supplier.objects.get(supplier_id=supplier_id)
        self.created_time = timezone.now()
        self.image_url = image_url
        self.hsn_code = hsn_code
        self.tax_code = Taxes.objects.get(tax_id=tax_id)
        self.save()
        item_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(self.item_id)
        self.item_code = item_code
        if len(bar_qr_code) == 0:
            self.code = item_code
        else:
            self.code = bar_qr_code
        self.save()
        return self.item_id, self.code

    def update(self, item_id: int, name: str, description: str, bar_qr_code: str, brand_id: int, category_id: int,
               supplier_id: int, image_url: str,hsn_code:str,tax_id:int):
        items = Items.objects.get(item_id=item_id)
        items.name = name
        items.description = description
        items.brand_id = Brand.objects.get(brand_id=brand_id)
        items.category_id = Category.objects.get(category_id=category_id)
        items.supplier_id = Supplier.objects.get(supplier_id=supplier_id)
        items.image_url = image_url
        items.hsn_code = hsn_code
        items.tax_code = Taxes.objects.get(tax_id=tax_id)
        if len(bar_qr_code) == 0:
            items.code = items.code
        else:
            self.code = bar_qr_code
        items.save()
        return items.item_id

    @staticmethod
    def remove(item_id: int):
        Items.objects.get(item_id=item_id).delete()

    @staticmethod
    def get(organisation_name: str, item_code: str = None, single: bool = False) -> list | dict:
        get_filter = Q(organisation_id__company_name=organisation_name)
        if item_code is not None:
            get_filter &= Q(item_code=item_code)
        if single:
            return Items.objects.filter(get_filter).values('name', 'description', 'code', 'is_active', 'item_code',
                                                           'brand_id__brand_code', 'brand_id__name',
                                                           'category_id__name', 'category_id__category_code',
                                                           'supplier_id__name', 'supplier_id__supplier_code',
                                                           'image_url','item_id','hsn_code','tax_code_id__name','tax_code_id__tax_code').first()
        return Items.objects.filter(get_filter).values(
            'name', 'description', 'code', 'is_active', 'item_code', 'brand_id__brand_code', 'brand_id__name',
            'category_id__name', 'category_id__category_code', 'supplier_id__name',
            'supplier_id__supplier_code', 'image_url', 'created_time','hsn_code','tax_code_id__name','tax_code_id__tax_code').order_by('name')

    @staticmethod
    def get_all(organisation_name: str, params: GetAll):
        filters = Q(organisation_id__company_name=organisation_name)
        if params.filter_key and params.filter_value:
            if params.filter_value == 'is_active':
                filters = filters & Q(**{params.filter_key: params.filter_value.lower() == 'true'})
            else:
                filters = filters & Q(**{params.filter_key: params.filter_value})

        if len(params.search_key) > 0:
            filters = filters & Q(name__icontains=params.search_key)

        return Items.objects.filter(filters).values(
            'name', 'description', 'code', 'is_active', 'item_code', 'brand_id__brand_code', 'brand_id__name',
            'category_id__name', 'category_id__category_code', 'supplier_id__name',
            'supplier_id__supplier_code', 'image_url', 'created_time').order_by(params.ordering)

    @staticmethod
    def get_with_item_list(organisation_name: str, item_code_list: list):
        return Items.objects.filter(item_code__in=item_code_list).values('item_code', 'itemversion__mrp_price',
                                                                         'item_id')

    @staticmethod
    def get_with_code(item_code: str, organisation_name: str) -> dict:
        return Items.objects.filter(item_code=item_code,
                                    organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
            'item_id').first()

    @staticmethod
    def get_with_code_list(item_code: list, organisation_name: str) -> list:
        return list(Items.objects.filter(item_code__in=item_code,
                                         organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
            'item_id'))

    @staticmethod
    def remove_from_list(item_ids: list) -> None:
        Items.objects.filter(item_id__in=item_ids).delete()
