import urllib
import uuid

from django.db import models
from django.db.models import Q

from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.organisation.models import Organisation


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    brand_code = models.CharField(max_length=50, default="", unique=True)
    secure = models.BooleanField(default=False)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'brand'

    def create(self, name: str, organisation_name: str, organisation_id: int, secure: bool = False) -> int:
        self.name = name
        self.organisation_id = Organisation(organisation_id)
        self.secure = secure
        if secure:
            code_id = str(uuid.uuid4())[-8:]
        else:
            self.save()
            code_id = self.brand_id
        org_initials = ''.join([i[0] for i in organisation_name.split()])

        brand_code = org_initials + '_' + str(code_id)

        self.brand_code = brand_code
        self.save()
        return self.brand_id

    @staticmethod
    def get(organisation_name: str,params:GetAll) -> list:
        filters= Q(organisation_id__company_name=organisation_name)

        if params.filter_key and params.filter_value:
            if params.filter_key.lower()== 'is_active':
                filters = filters & Q(is_active=params.filter_value.lower() == 'true')
            else:
                filters=filters & Q(**{params.filter_key:params.filter_value})
        
        if len(params.search_key)>0:
            filters=filters & Q(name__icontains=params.search_key)
        return Brand.objects.filter(filters).values('name', 'brand_code').order_by(params.ordering)

    @staticmethod
    def get_with_code(brand_code: str, organisation_name: str) -> dict:
        return Brand.objects.filter(brand_code=brand_code,
                                    organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
            'brand_id').first()

    @staticmethod
    def get_with_code_list(brand_code: list, organisation_name: str) -> list:
        return list(Brand.objects.filter(brand_code__in=brand_code,
                                         organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
            'brand_id'))

    @staticmethod
    def remove(brand_id: int) -> None:
        Brand.objects.get(brand_id=brand_id).delete()

    @staticmethod
    def remove_from_list(brand_ids: list) -> None:
        Brand.objects.filter(brand_id__in=brand_ids).delete()

    @staticmethod
    def update(brand_id: int, name: str) -> None:
        brand = Brand.objects.get(brand_id=brand_id)
        brand.name = name
        brand.save()

    @staticmethod
    def brand_check_name_exist(name:str,organisation_name:str):
        resp =  Brand.objects.filter(name=name,organisation_id__company_name=urllib.parse.unquote(organisation_name)).exists()
        if resp:
            raise ValueError("Brand name already exist")


    @staticmethod
    def get_sorted_brands(organisation_name: str, sort_order: str) -> list:
        order_by = 'name' if sort_order == 'asc' else '-name'
        return Brand.objects.filter(organisation_id__company_name=organisation_name).values('name', 'brand_code').order_by(
            order_by)
