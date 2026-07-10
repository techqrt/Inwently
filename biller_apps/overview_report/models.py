from django.db import models
from django.utils import timezone
from biller_apps.organisation.models import Organisation
from biller_apps.item.models.items import Items
from biller_apps.brand.models import Brand
from biller_apps.supplier.models import Supplier
from biller_apps.category.models import Category
from biller_apps.customer.models import Customer

class OverviewReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'overview_report'
    
    @staticmethod
    def get_overview_reports(organisation_name: str, start_date: str, end_date: str) -> list:
        return Items.objects.filter(
            organisation_id__company_name=organisation_name,
            created_time__range=[start_date, end_date]
        ).values(
            'description', 'code', 'is_active', 'item_code', 'created_time', 'image_url',
            'brand_id__name', 'brand_id__brand_code',
            'supplier_id__name', 'supplier_id__supplier_code',
            'category_id__name', 'category_id__category_code'
        ).order_by('-created_time')
    
    @staticmethod
    def get_customer_overview_reports(organisation_name: str, start_date: str, end_date: str) -> list:
        return Customer.objects.filter(
            organisation_id__company_name=organisation_name,
            created_date_time__range=[start_date, end_date]
        ).values(
            'customer_id', 'name', 'mobile_number', 'email_id', 'customer_code',
            'date_of_birth', 'gender', 'martial_status', 'religion', 'blood_group', 'education',
            'occupation', 'is_active', 'created_date_time',
            'photo_url', 'id_proof_url'
        ).order_by('-created_date_time')
    
    @staticmethod
    def get_supplier_overview_reports(organisation_name: str, start_date: str, end_date: str) -> list:
        return Supplier.objects.filter(
            organisation_id__company_name=organisation_name,
            created_date_time__range=[start_date, end_date]
        ).values(
            'supplier_id', 'name', 'mobile_number', 'email_id', 'supplier_code',
            'gst_number', 'id_number', 'id_type', 'is_active', 'created_date_time',
            'photo_url', 'id_proof_url'
        ).order_by('-created_date_time')
