from django.db import models
from django.utils import timezone
from biller_apps.organisation.models import Organisation
from biller_apps.employees.models.employees import Employees


class AdminReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'admin_report'

    @staticmethod
    def get_admin_reports(organisation_name: str, start_date: str, end_date: str) -> list:
        return Employees.objects.filter(
            organisation_id__company_name=organisation_name,
            created_date_time__range=[start_date, end_date]
        ).values(
            'employee_id', 'name', 'mobile_number', 'alternate_mobile_number',
            'dob', 'employee_code', 'email_verified', 'created_date_time',
            'is_active', 'is_active_change_time', 'profile_photo_url',
            'address_id__street', 'address_id__state', 'address_id__country'
        ).order_by('-created_date_time')
