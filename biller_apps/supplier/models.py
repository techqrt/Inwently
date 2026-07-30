import urllib

from django.db import models
from django.utils import timezone
from django.db.models import Q
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.models.adress import Address
from biller_apps.organisation.models import Organisation


class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    address_id = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created_date_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_active_change_time = models.DateTimeField(default=timezone.now)
    mobile_number = models.CharField(max_length=20, default='', unique=True)
    alt_mobile_number = models.CharField(max_length=20, default='', null=True)
    id_number = models.CharField(max_length=100, default='')
    id_type = models.CharField(max_length=100, default='')
    gst_number = models.CharField(max_length=100, default='')
    email_id = models.EmailField(default='', unique=True)
    supplier_code = models.CharField(max_length=10, default='', unique=True)
    photo_url = models.CharField(default=None, null=True,max_length=200)
    id_proof_url = models.CharField(default=None, null=True,max_length=200)
    secure = models.BooleanField(default=False)

    class Meta:
        db_table = 'supplier'

    def create(self, name: str, mobile_number: str, email_id: str, alt_mobile_number: str, id_number: str, id_type: str,
               gst_number: str, photo_url: str, id_proof_url: str, organisation_id: int, organisation_name: str,
               address_id: int, secure: bool = False) -> int:
        self.name = name
        self.address_id = Address(address_id)
        self.organisation_id = Organisation(organisation_id)
        self.created_date_time = timezone.now()
        self.is_active = True
        self.is_active_change_time = timezone.now()
        self.mobile_number = mobile_number
        self.email_id = email_id
        self.alt_mobile_number = alt_mobile_number
        self.id_number = id_number
        self.id_type = id_type
        self.gst_number = gst_number
        self.photo_url = photo_url
        self.id_proof_url = id_proof_url
        self.secure = secure
        self.save()
        self.supplier_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(
            self.supplier_id)
        self.save()
        return self.supplier_id

    @staticmethod
    def update(supplier_id: int, name: str, mobile_number: str, email_id: str, alt_mobile_number: str, id_number: str,
               id_type: str, gst_number: str, photo_url: str, id_proof_url: str) -> int:
        supplier = Supplier.objects.get(supplier_id=supplier_id)
        supplier.name = name
        supplier.mobile_number = mobile_number
        supplier.email_id = email_id
        supplier.alt_mobile_number = alt_mobile_number
        supplier.id_number = id_number
        supplier.id_type = id_type
        supplier.gst_number = gst_number
        supplier.photo_url = photo_url
        supplier.id_proof_url = id_proof_url
        supplier.save()
        return supplier.supplier_id

    @staticmethod
    def get(organisation_name: str, supplier_code: str, single: bool = False) -> list | dict:
        if single:
            return Supplier.objects.filter(supplier_code=supplier_code,
                                           organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
                'address_id', 'supplier_id').first()
        return Supplier.objects.filter(organisation_id__company_name=organisation_name, supplier_code=supplier_code).values(
            'organisation_id__company_name', 'address_id__country', 'address_id__state', 'address_id__street', 'name',
            'is_active', 'mobile_number', 'email_id', 'created_date_time', 'alt_mobile_number',
            'supplier_code', 'id_number', 'id_type', 'gst_number', 'photo_url', 'id_proof_url').order_by('name')

    @staticmethod
    def get_by_mobile(organisation_name: str, mobile_number: str) -> dict:
        return Supplier.objects.filter(mobile_number=mobile_number,
                                       organisation_id__company_name=urllib.parse.unquote(organisation_name)).values().first()

    @staticmethod
    def get_by_email(organisation_name: str, email: str) -> dict:
        return Supplier.objects.filter(email_id=email,
                                       organisation_id__company_name=urllib.parse.unquote(organisation_name)).values().first()

    @staticmethod
    def get_all(organisation_name: str,params:GetAll)->list:
        filters=Q(organisation_id__company_name=organisation_name)
        if params.filter_key and params.filter_value:
            if params.filter_key.lower() == 'is_active':
                filters &= Q(is_active=params.filter_value.lower() == 'true'        )
            else:
                filters &= Q(**{params.filter_key: params.filter_value})
        if len(params.search_key) > 0:
            filters &= Q(name__icontains=params.search_key) 
        return Supplier.objects.filter(filters).values(
            'organisation_id__company_name', 'address_id__country', 'address_id__state', 'address_id__street', 'name',
            'is_active', 'mobile_number', 'email_id', 'created_date_time', 'alt_mobile_number',
            'supplier_code', 'id_number', 'id_type', 'gst_number', 'photo_url', 'id_proof_url').order_by(params.ordering)

    @staticmethod
    def remove(supplier_id: int):
        Supplier.objects.get(supplier_id=supplier_id).delete()

    @staticmethod
    def get_with_code_list(supplier_code: list, organisation_name: str) -> list:
        return list(Supplier.objects.filter(supplier_code__in=supplier_code,
                                            organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
            'supplier_id', 'address_id'))

    @staticmethod
    def remove_from_list(supplier_codes: list) -> None:
        Supplier.objects.filter(supplier_code__in=supplier_codes).delete()

    @staticmethod
    def get_sorted_suppliers(organisation_name: str, sort_order: str) -> list:
        order_by = 'name' if sort_order == 'asc' else '-name'
        return Supplier.objects.filter(organisation_id__company_name=organisation_name).values('name',
                                                                                       'supplier_code').order_by(
            order_by)
    
