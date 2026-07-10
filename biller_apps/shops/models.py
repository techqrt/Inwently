import urllib

from django.db import models
from django.db.models import Q
from django.utils import timezone

from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.models.adress import Address
from biller_apps.organisation.models import Organisation


class Shops(models.Model):
    shop_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    address_id = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created_date_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_active_change_time = models.DateTimeField(default=timezone.now)
    shop_code = models.CharField(max_length=10, default='')
    website = models.TextField(default=None, null=True)
    email_id = models.CharField(max_length=50, default=None, null=True)
    mobile_number = models.CharField(max_length=20, default=None, null=True)
    alt_mobile_number = models.CharField(max_length=20, default=None, null=True)
    type = models.CharField(max_length=100, default='branch')

    class Meta:
        db_table = 'shops'

    def create(self, name: str, organisation_name: str, organisation_id: int, address_id: int, website: str,
               email_id: str, mobile_number: str, alt_mobile_number: str, type: str) -> int:
        self.name = name
        self.address_id = Address(address_id)
        self.organisation_id = Organisation(organisation_id)
        self.created_date_time = timezone.now()
        self.is_active = True
        self.is_active_change_time = timezone.now()
        self.website = website
        self.email_id = email_id
        self.mobile_number = mobile_number
        self.alt_mobile_number = alt_mobile_number
        self.type = type
        self.save()
        print(organisation_name)
        self.shop_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(self.shop_id)
        self.save()
    
        return self.shop_id

    @staticmethod
    def get(name: str, organisation_id: int, single: bool = False) -> dict | list:
        if single:
            return Shops.objects.filter(Q(name=name) & Q(organisation_id_id=organisation_id)).values().first()
        return Shops.objects.filter(Q(name=name) & Q(organisation_id_id=organisation_id)).values()

    @staticmethod
    def get_by_code(shop_code: str) -> list:
        return Shops.objects.filter(shop_code=shop_code).values(
            'name', 'is_active', 'organisation_id_id__company_name', 'created_date_time', 'is_active_change_time', 'shop_code', 'website',
            'email_id', 'mobile_number', 'alt_mobile_number', 'type')

    @staticmethod
    def get_by_name_list(name: list) -> list:
        return Shops.objects.filter(name__in=name).values('shop_id')

    @staticmethod
    def get_with_code(shop_code: str, organisation_name: str):
        return Shops.objects.filter(organisation_id_id__company_name=organisation_name, shop_code=shop_code).values().first()

    @staticmethod
    def get_all(organisation_name: str, type: str,params:GetAll) -> list:
        filter_criteria = Q(organisation_id_id__company_name=organisation_name)
        if params.filter_key and params.filter_value:
            if params.filter_value=='is_active':
                filter_criteria &= Q(**{params.filter_value:params.filter_value.lower()=='true'})
            else:
                filter_criteria &= Q(**{params.filter_key:params.filter_value})
        if len(params.search_key) > 0:
            filter_criteria &= Q(name__icontains=params.search_keys)
        if type == 'branch':
            filter_criteria &= Q(type='branch')
        elif type == 'warehouse':
            filter_criteria &= Q(type='warehouse')

        return Shops.objects.filter(filter_criteria).values(
            'name', 'is_active', 'organisation_id_id__company_name', 'created_date_time', 'address_id_id__state',
            'address_id_id__street', 'address_id_id__country', 'is_active_change_time', 'shop_code', 'website',
            'email_id', 'mobile_number', 'alt_mobile_number', 'type').order_by(params.ordering)

    @staticmethod
    def update(name: str, shop_id: int, email_id: str, mobile_number: str,alt_mobile_number: str, website: str, type: str) -> int:
        shop = Shops.objects.get(shop_id=shop_id)
        shop.name = name
        shop.email_id = email_id
        shop.mobile_number = mobile_number
        shop.alt_mobile_number = alt_mobile_number
        shop.website = website
        shop.type = type
        shop.save()
        return shop.shop_id

    @staticmethod
    def remove(shop_id: int) -> None:
        Shops.objects.get(shop_id=shop_id).delete()

    @staticmethod
    def get_count(organization_name: str) -> int:
        return Shops.objects.filter(organisation_id__company_name=organization_name).count()

    @staticmethod
    def get_with_code_list(shop_code: list, organisation_name: str) -> list:
        return list(Shops.objects.filter(organisation_id_id__company_name=organisation_name, shop_code__in=shop_code).values('shop_id'))

    @staticmethod
    def remove_from_list(shop_id: list) -> None:
        Shops.objects.filter(shop_id__in=shop_id).delete()

    @staticmethod
    def get_by_ids(shop_ids: list) -> list:
        return Shops.objects.filter(shop_id__in=shop_ids, is_active=True).values('name', 'shop_code')
