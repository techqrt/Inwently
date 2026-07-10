import datetime
from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import date
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.models.adress import Address



class Organisation(models.Model):
    organisation_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100, default='')
    address_id = models.ForeignKey(Address, on_delete=models.DO_NOTHING,default=1)
    owner_name = models.CharField(max_length=100, default='')
    owner_mobile = models.CharField(max_length=20, default='')
    owner_alternate_mobile = models.CharField(max_length=20, default='')
    owner_email = models.CharField(max_length=30, default='')
    created_date_time = models.DateTimeField(default=timezone.now)
    shop_count = models.IntegerField(default=0)
    employee_count = models.IntegerField(default=0)
    approval = models.BooleanField(default=False)
    plan = models.CharField(max_length=100,default='CUSTOM')
    plan_expiry = models.DateTimeField(default=timezone.now)
    payment_gateway = models.BooleanField(default=False)


    class Meta:
        db_table = 'organisation'

    def create(self,company_name:str, owner_name: str, owner_mobile: str, address_id: int, shop_count: int,owner_email: str,
               employee_count: int,approval: bool=False,  owner_alternate_mobile:str= '',plan: str='CUSTOM', plan_expiry: datetime.datetime=datetime.datetime.now(tz=datetime.timezone.utc)) -> int:
        self.owner_name = owner_name
        self.owner_mobile = owner_mobile
        self.company_name = company_name
        self.owner_alternate_mobile = owner_alternate_mobile
        self.owner_email = owner_email
        self.address_id = Address(address_id)
        self.created_date_time = datetime.datetime.now(datetime.timezone.utc)
        self.shop_count = shop_count
        self.employee_count = employee_count
        self.approval = approval
        self.plan = plan
        self.plan_expiry = plan_expiry
        self.save()
        return self.organisation_id

    @staticmethod
    def update(owner_name: str, owner_mobile: str, company_name: str, organisation_id: int, shop_count: int,owner_email: str,
               employee_count: int, approval: bool, plan: str, plan_expiry: date, owner_alternate_mobile: str) -> int:
        organisation = Organisation.objects.get(organisation_id=organisation_id)
        organisation.owner_name = owner_name
        organisation.company_name = company_name
        organisation.owner_alternate_mobile = owner_alternate_mobile
        organisation.owner_email = owner_email
        organisation.owner_mobile = owner_mobile
        organisation.shop_count = shop_count
        organisation.employee_count = employee_count
        organisation.approval = approval
        organisation.plan = plan
        organisation.plan_expiry = plan_expiry
        organisation.save()
        return organisation.organisation_id

    @staticmethod
    def remove(organisation_id: int) -> None:
        Organisation.objects.get(organisation_id=organisation_id).delete()

    @staticmethod
    def remove_from_list(organisation_ids: list) -> None:
        Organisation.objects.filter(organisation_id__in=organisation_ids).delete()


    @staticmethod
    def get(company_name: str, single: bool = False) -> list | dict:
        if single:
            return Organisation.objects.filter(company_name=company_name).values('owner_name', 'owner_mobile', 'owner_alternate_mobile' ,'company_name',
                                                             'created_date_time', 'shop_count', 'employee_count','owner_email'
                                                             ,'approval','plan','plan_expiry','organisation_id').first()or[]
        return Organisation.objects.filter(company_name=company_name).values('owner_name', 'owner_mobile', 'owner_alternate_mobile' ,'company_name',
                                                             'created_date_time', 'shop_count', 'employee_count'
                                                             ,'approval','plan','plan_expiry','organisation_id','owner_email')or[]


    @staticmethod
    def get_all(organisation_name: str,params:GetAll) -> list:
        filters = Q(company_name=organisation_name)
        if params.filter_key and params.filter_value:
            if params.filter_value=='is_active':
                filters&=Q(**{params.filter_key:params.filter_value.lower()=='true'})
            else:
                filters&=Q(**{params.filter_key:params.filter_value})
        if len(params.search_key)>0:
            filters&=Q(company_name__icontains=params.search_key)
        if params.sort_by == 'name':
            params.sort_by = 'company_name'
            ordering = f"{'-' if params.sort_order == 'desc' else ''}{params.sort_by}"
        
        return Organisation.objects.filter(company_name=organisation_name).values('owner_name', 'owner_mobile', 'owner_alternate_mobile' ,'company_name',
                                                                  'created_date_time',
                                                                  'shop_count', 'employee_count', 'approval','plan','plan_expiry')or[]

class Version(models.Model):
    """Model to store version details for the application."""
    
    repo_url = models.URLField(help_text="Base URL for downloading versions", null=True, blank=True)
    file_name = models.CharField(max_length=255, help_text="Name of the installer file", null=True, blank=True)
    minimum_version = models.JSONField(help_text="Minimum required version details", null=False, blank=False)
    latest_stable_version = models.JSONField(help_text="Latest stable version details", null=False, blank=False)
    previous_stable_version = models.JSONField(help_text="Previous stable version details", null=False, blank=False)
    beta_version = models.JSONField(null=True, blank=True, help_text="Beta version details")
    other_versions = models.JSONField(null=True, blank=True, help_text="List of other versions")
    changes_in_latest_stable = models.JSONField(help_text="List of changes in the latest stable version", null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now, help_text="Timestamp when the version was created")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'version'
        ordering = ['-created_at']
        verbose_name = "Version"
        verbose_name_plural = "Versions"

    @staticmethod
    def create_version(repo_url, file_name, minimum_version, latest_stable_version, 
                      previous_stable_version, beta_version=None, other_versions=None, 
                      changes_in_latest_stable=None):
        """Create a new version record"""
        return Version.objects.create(
            repo_url=repo_url,
            file_name=file_name,
            minimum_version=minimum_version,
            latest_stable_version=latest_stable_version,
            previous_stable_version=previous_stable_version,
            beta_version=beta_version,
            other_versions=other_versions,
            changes_in_latest_stable=changes_in_latest_stable
        )