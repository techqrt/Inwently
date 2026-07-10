import datetime
import urllib

from django.db import models
from django.db.models import Q
from django.utils import timezone

from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.models.adress import Address
from biller_apps.organisation.models import Organisation


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    address_id = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created_date_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_active_change_time = models.DateTimeField(default=timezone.now)
    mobile_number = models.CharField(max_length=20, default='', unique=True)
    id_number = models.CharField(max_length=100, default=None, null=True)
    id_type = models.CharField(max_length=100, default=None, null=True)
    email_id = models.EmailField(default=None, unique=True, null=True)
    customer_code = models.CharField(max_length=10, default='', unique=True)
    photo_url = models.CharField(max_length=350, default=None, null=True)
    id_proof_url = models.CharField(max_length=350, default=None, null=True)
    occupation = models.CharField(max_length=100, default=None, null=True)
    date_of_birth = models.DateField(default=None, null=True)
    gender = models.CharField(max_length=1, default=None, null=True)
    martial_status = models.CharField(max_length=100, default=None, null=True)
    religion = models.CharField(max_length=100, default=None, null=True)
    blood_group = models.CharField(max_length=100, default=None, null=True)
    education = models.CharField(max_length=100, default=None, null=True)
    secure = models.BooleanField(default=False)

    class Meta:
        db_table = 'customer'

    def create(self, name: str, mobile_number: str, organisation_name: str, organisation_id: int, address_id: int,
               id_number: str = None, id_type: str = None, email_id: str = None, photo_url: str = None,
               id_proof_url: str = None, occupation: str = None, date_of_birth: datetime.date = None,
               gender: str = None, martial_status: str = None, religion: str = None, blood_group: str = None,
               education: str = None, secure: bool = False):
        self.name = name
        self.mobile_number = mobile_number
        self.organisation_id = Organisation(organisation_id)
        self.is_active = True
        self.id_number = id_number
        self.id_type = id_type
        self.email_id = email_id
        self.photo_url = photo_url
        self.id_proof_url = id_proof_url
        self.occupation = occupation
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.martial_status = martial_status
        self.religion = religion
        self.blood_group = blood_group
        self.education = education
        self.address_id = Address(address_id)
        self.secure = secure
        self.save()
        self.customer_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(self.customer_id)
        self.save()
        return self.customer_id

    @staticmethod
    def get_by_mobile(organisation_name: str, mobile_number: str) -> dict:
        return Customer.objects.filter(mobile_number=mobile_number,
                                       organisation_id__company_name=urllib.parse.unquote(organisation_name)).values().first()

    @staticmethod
    def get_by_email(organisation_name: str, email: str) -> dict:
        return Customer.objects.filter(email_id=email,
                                       organisation_id__company_name=urllib.parse.unquote(organisation_name)).values().first()

    @staticmethod
    def get_all(organisation_name: str, params:GetAll) -> list:
        filters= Q(organisation_id__company_name=organisation_name)

        if params.filter_key and params.filter_value:
            if params.filter_value=='is_active':
                filters=filters & Q(**{params.filter_key:params.filter_value.lower()=='true'})
            else:
                filters=filters & Q(**{params.filter_key:params.filter_value})
                
        if len(params.search_key)>0:
            filters=filters & Q(name__icontains=params.search_key)
            
        return Customer.objects.filter(filters).values(
            'organisation_id__company_name', 'address_id__country', 'address_id__state', 'address_id__street', 'name',
            'is_active', 'mobile_number', 'email_id', 'created_date_time', 'customer_code', 'id_number', 'id_type',
            'occupation', 'photo_url', 'id_proof_url', 'date_of_birth', 'gender', 'martial_status', 'religion',
            'blood_group', 'education').order_by(params.ordering)

    @staticmethod
    def get(organisation_name: str, customer_code: str, single: bool = False) -> list | dict:
        if single:
            return Customer.objects.filter(customer_code=customer_code,
                                           organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
                'address_id', 'customer_id').first()
        return Customer.objects.filter(organisation_id__company_name=organisation_name, customer_code=customer_code).values(
            'organisation_id__company_name', 'address_id__country', 'address_id__state', 'address_id__street', 'name',
            'is_active', 'mobile_number', 'email_id', 'created_date_time', 'customer_code', 'id_number', 'id_type',
            'occupation', 'photo_url', 'id_proof_url', 'date_of_birth', 'gender', 'martial_status', 'religion',
            'blood_group', 'education').order_by('name')

    @staticmethod
    def update(customer_id: int, name: str, mobile_number: str, id_number: str, id_type: str, email_id: str,
               photo_url: str, id_proof_url: str, occupation: str, date_of_birth: datetime.date, gender: str,
               martial_status: str, religion: str, blood_group: str, education: str):
        customer = Customer.objects.get(customer_id=customer_id)
        customer.name = name
        customer.mobile_number = mobile_number
        customer.id_number = id_number
        customer.id_type = id_type
        customer.email_id = email_id
        customer.photo_url = photo_url
        customer.id_proof_url = id_proof_url
        customer.occupation = occupation
        customer.date_of_birth = date_of_birth
        customer.gender = gender
        customer.martial_status = martial_status
        customer.religion = religion
        customer.blood_group = blood_group
        customer.education = education
        customer.save()
        return customer.customer_id

    @staticmethod
    def remove(customer_id: int):
        Customer.objects.get(customer_id=customer_id).delete()

    @staticmethod
    def get_with_code_list(customer_code: list, organisation_name: str) -> list:
        return list(Customer.objects.filter(customer_code__in=customer_code,
                                            organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
            'customer_id', 'address_id'))

    @staticmethod
    def remove_from_list(customer_id: list) -> None:
        Customer.objects.filter(customer_id__in=customer_id).delete()
