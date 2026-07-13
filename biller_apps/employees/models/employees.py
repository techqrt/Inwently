import datetime
import urllib

from django.db import models
from django.db.models import Q
from django.utils import timezone


from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.models.adress import Address
from biller_apps.employees.models.employee_credentials import EmployeeCredentials
from biller_apps.employees.models.permission import SalesPermission, PrinterTemplatesPermission, ReportsPermission, \
    PurchasePermission, DashboardPermission, InventoryPermission, MasterDataPermission, QuotationsPermission
from biller_apps.organisation.models import Organisation


class Employees(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    mobile_number = models.CharField(max_length=20, default='', unique=True)
    alternate_mobile_number = models.CharField(max_length=20, default=None, null=True, blank=True, unique=True)
    dob = models.DateField(default='')
    address_id = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    shop_access = models.JSONField(default=list)
    dashboard_permission = models.ForeignKey(DashboardPermission, on_delete=models.DO_NOTHING, null=True)
    master_data_permission = models.ForeignKey(MasterDataPermission, on_delete=models.DO_NOTHING, null=True)
    inventory_permission = models.ForeignKey(InventoryPermission, on_delete=models.DO_NOTHING, null=True)
    sales_permission = models.ForeignKey(SalesPermission, on_delete=models.DO_NOTHING, null=True)
    quotations_permission = models.ForeignKey(QuotationsPermission, on_delete=models.DO_NOTHING, null=True)
    printer_templates_permission = models.ForeignKey(PrinterTemplatesPermission, on_delete=models.DO_NOTHING, null=True)
    purchase_permission = models.ForeignKey(PurchasePermission, on_delete=models.DO_NOTHING, null=True)
    reports_permission = models.ForeignKey(ReportsPermission, on_delete=models.DO_NOTHING, null=True)
    is_active = models.BooleanField(default=False)
    is_active_change_time = models.DateTimeField(default=timezone.now)
    access_token = models.TextField(default='')
    refresh_token = models.TextField(default='')
    employee_code = models.CharField(max_length=10, default='', unique=True)
    email_verified = models.BooleanField(default=False)
    created_date_time = models.DateTimeField(default=timezone.now)
    employee_credentials_id = models.ForeignKey(EmployeeCredentials, on_delete=models.DO_NOTHING)
    token_key = models.TextField(default='')
    profile_photo_url = models.CharField(default=None, null=True,max_length=200)
    secure = models.BooleanField(default=False)
    otp = models.IntegerField(default=0, null=True)
    otp_expiry = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        db_table = 'employees'

    def create(self, name: str, mobile_number: str, dob: datetime, shop_access: list, organisation_name,
               address_id: int, organisation_id: int, credentials_id: int, profile_photo_url: str,
               dashboard_permission_id: int, master_data_permission_id: int,
               inventory_permission_id: int, sales_permission_id: int, quotations_permission_id: int,
               printer_templates_permission_id: int, purchase_permission_id: int, reports_permission_id: int,
               is_active: bool = False, secure: bool = False, token_key: str = "", refresh_token: str = "", alternate_mobile_number: str=None) -> int:
        self.name = name
        self.mobile_number = mobile_number
        self.alternate_mobile_number = alternate_mobile_number
        self.dob = dob
        self.shop_access = shop_access
        self.address_id_id = address_id
        self.organisation_id_id = organisation_id
        self.is_active = is_active
        self.email_verified = False
        self.created_date_time = timezone.now()
        self.is_active_change_time = timezone.now()
        self.employee_credentials_id_id = credentials_id
        self.profile_photo_url = profile_photo_url
        self.secure = secure
        self.token_key = token_key
        self.refresh_token = refresh_token
        self.dashboard_permission = DashboardPermission(dashboard_permission_id)
        self.master_data_permission = MasterDataPermission(master_data_permission_id)
        self.inventory_permission = InventoryPermission(inventory_permission_id)
        self.sales_permission = SalesPermission(sales_permission_id)
        self.quotations_permission = QuotationsPermission(quotations_permission_id)
        self.printer_templates_permission = PrinterTemplatesPermission(printer_templates_permission_id)
        self.purchase_permission = PurchasePermission(purchase_permission_id)
        self.reports_permission = ReportsPermission(reports_permission_id)
        self.save()
        self.employee_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(self.employee_id)
        self.save()
        return self.employee_id

    @staticmethod
    def update(employee_id: int, name: str, mobile_number: str, alternate_mobile_number: str, dob: datetime, shop_access: list,
               profile_photo_url: str) -> int:
        employee = Employees.objects.get(employee_id=employee_id)
        employee.name = name
        employee.mobile_number = mobile_number
        employee.alternate_mobile_number = alternate_mobile_number
        employee.dob = dob
        employee.shop_access = shop_access
        employee.profile_photo_url = profile_photo_url
        employee.save()
        return employee.employee_id



    @staticmethod
    def update_activation(employee_id: int, is_active: bool, email_verified: bool) -> int:
        employees = Employees.objects.get(employee_id=employee_id)
        employees.is_active = is_active
        employees.email_verified = email_verified
        employees.is_active_change_time = timezone.now()
        employees.otp=None
        employees.otp_expiry=None
        employees.save()
        return employees.employee_id

    @staticmethod
    def remove(employee_id: int) -> None:
        Employees.objects.get(employee_id=employee_id).delete()

    @staticmethod
    def get_connections(employee_code: str, organisation_name: str):
        return Employees.objects.filter(
            Q(employee_code=employee_code) & Q(organisation_id__company_name=organisation_name)).values(
            'employee_id', 'address_id_id', 'dashboard_permission_id', 'inventory_permission_id',
            'master_data_permission_id', 'sales_permission_id', 'quotations_permission_id',
            'printer_templates_permission_id', 'purchase_permission_id', 'reports_permission_id').first()

    @staticmethod
    def get(employee_code: str, organisation_name: str) -> dict:
        return Employees.objects.filter(employee_code=employee_code, organisation_id__company_name=organisation_name).values(
            'name', 'mobile_number', 'alternate_mobile_number', 'dob', 'address_id_id__state', 'address_id_id__country', 'organisation_id__company_name',
            'shop_access', 'address_id_id__street', 'dashboard_permission__dashboard',
            'master_data_permission__item', 'master_data_permission__supplier', 'master_data_permission__shop',
            'master_data_permission__customer',
            'master_data_permission__employee', 'master_data_permission__creating', 'inventory_permission__inventory',
            'sales_permission__pos', 'sales_permission__return_item', 'sales_permission__bill_history',
            'quotations_permission__quotations', 'printer_templates_permission__printer_templates',
            'purchase_permission__purchase_list',
            'purchase_permission__return_purchase', 'purchase_permission__stock', 'purchase_permission__stock',
            'reports_permission__general', 'reports_permission__overview', 'reports_permission__administration',
            'reports_permission__day_book', 'reports_permission__gst',
            'is_active', 'employee_credentials_id__email_id', 'email_verified', 'employee_code',
            'profile_photo_url').first()

    @staticmethod
    def get_all(organisation_name: str,params:GetAll) -> list:
        filters =  Q(organisation_id__company_name=organisation_name)

        if params.filter_key and params.filter_value:
            if params.filter_key == 'is_active':
                filters = filters & Q(**{params.filter_key: params.filter_value.lower() == 'true'})
            else:
                filters = filters & Q(**{params.filter_key: params.filter_value})

        if len(params.search_key)>0:
            filters = filters & Q(name__icontains=params.search_key)


        return Employees.objects.filter(filters).values(
            'name', 'mobile_number', 'alternate_mobile_number', 'dob', 'address_id_id__state', 'address_id_id__country', 'address_id_id__street',
            'dashboard_permission__dashboard',
            'master_data_permission__item', 'master_data_permission__supplier', 'master_data_permission__shop',
            'master_data_permission__customer',
            'master_data_permission__employee', 'master_data_permission__creating', 'inventory_permission__inventory',
            'sales_permission__pos', 'sales_permission__return_item', 'sales_permission__bill_history',
            'quotations_permission__quotations', 'printer_templates_permission__printer_templates',
            'purchase_permission__purchase_list',
            'purchase_permission__return_purchase', 'purchase_permission__stock', 'purchase_permission__stock',
            'reports_permission__general', 'reports_permission__overview', 'reports_permission__administration',
            'reports_permission__day_book', 'reports_permission__gst',
            'is_active', 'employee_credentials_id__email_id', 'email_verified', 'profile_photo_url',
            'organisation_id__company_name', 'employee_code').order_by(params.ordering)

    @staticmethod
    def get_by_email(email: str, organisation_name: str) -> dict:
        return Employees.objects.filter(employee_credentials_id__email_id=email,
                                        organisation_id__company_name=organisation_name).values().first()

    @staticmethod
    def get_by_mobile(mobile_number: str, organisation_name: str, exclude_employee_id: int=None) -> dict:
        filter = Q(mobile_number=mobile_number) & Q(organisation_id__company_name=organisation_name)
        if exclude_employee_id is not None:
            filter = filter & ~Q(employee_id=exclude_employee_id)
        return Employees.objects.filter(filter).values().first()

    @staticmethod
    def get_login_auth(employee_credentials_id: int) -> dict:
        return Employees.objects.filter(employee_credentials_id_id=employee_credentials_id, is_active=True).values(
            'employee_id', 'organisation_id__company_name', 'name', 'employee_code', 'dashboard_permission__dashboard',
            'master_data_permission__item', 'master_data_permission__supplier', 'master_data_permission__shop',
            'master_data_permission__customer',
            'master_data_permission__employee', 'master_data_permission__creating', 'inventory_permission__inventory',
            'sales_permission__pos', 'sales_permission__return_item', 'sales_permission__bill_history',
            'quotations_permission__quotations', 'printer_templates_permission__printer_templates',
            'purchase_permission__purchase_list',
            'purchase_permission__return_purchase', 'purchase_permission__stock', 'purchase_permission__stock',
            'reports_permission__general', 'reports_permission__overview', 'reports_permission__administration',
            'reports_permission__day_book', 'reports_permission__gst',
            'employee_credentials_id__email_id', 'shop_access', 'organisation_id__approval',
            'profile_photo_url').first()

    @staticmethod
    def update_tokens(employee_id: int, access_token: str, refresh_token: str, token_key: str) -> int:
        employee = Employees.objects.get(employee_id=employee_id)
        employee.access_token = access_token
        employee.refresh_token = refresh_token
        employee.token_key = token_key
        employee.save()
        return employee.employee_id

    @staticmethod
    def get_by_id(employee_credentials_id: int) -> dict:
        return Employees.objects.filter(employee_credentials_id_id=employee_credentials_id).values(
            'refresh_token', 'access_token', 'organisation_id__company_name', 'employee_id').first()

    @staticmethod
    def update_access_token(employee_id: int, access_token: str):
        employee = Employees.objects.get(employee_id=employee_id)
        employee.access_token = access_token
        employee.save()
        return employee.employee_id
    @staticmethod
    def update_otp(employee_id: int,otp: int,expiry: datetime):
        employee = Employees.objects.get(employee_id=employee_id)
        employee.otp = otp
        employee.otp_expiry = expiry
        employee.save()
        return employee.employee_id

    @staticmethod
    def get_count(organisation_name: str) -> int:
        return Employees.objects.filter(organisation_id__company_name=organisation_name).count()

    @staticmethod
    def get_with_code_list(employee_code: list, organisation_name: str) -> list:
        return list(Employees.objects.filter(employee_code__in=employee_code,
                                             organisation_id__company_name=urllib.parse.unquote(organisation_name)).values(
            'employee_id', 'address_id', 'employee_credentials_id'))

    @staticmethod
    def remove_from_list(employee_id: list) -> None:
        Employees.objects.filter(employee_id__in=employee_id).delete()

    @staticmethod
    def status_change_from_list(employee_id: list,status:bool) -> None:
        Employees.objects.filter(employee_id__in=employee_id).update(is_active=status)

    @staticmethod
    def get_by_refresh_token(refresh_token: str) -> dict:
        return Employees.objects.filter(refresh_token=refresh_token).values('token_key', 'employee_id').first()
    @staticmethod
    def get_by_id_except_one(employee_id:int,email_id:str):
        return Employees.objects.filter(~Q(employee_id=employee_id)&Q(employee_credentials_id__email_id=email_id)).values('employee_credentials_id').first()

    @staticmethod
    def get_by_email_dob_code(employee_code:str,email_id:str,dob:datetime):
        return Employees.objects.filter(employee_code=employee_code,employee_credentials_id__email_id=email_id,dob=dob).values().first()

    @staticmethod
    def get_with_email(email_id: str) -> dict:
        return Employees.objects.filter(employee_credentials_id__email_id=email_id).values().first()

    @staticmethod
    def get_by_email_and_otp(email_id:str,otp:int):
        return Employees.objects.filter(employee_credentials_id__email_id=email_id,otp=otp).values().first()

