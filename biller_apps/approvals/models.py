import datetime

from django.db import models

from biller_apps.employees.models.employees import Employees
from biller_apps.organisation.models import Organisation


class Approvals(models.Model):
    approval_id = models.AutoField(primary_key=True)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    request_from = models.EmailField(max_length=30, default='')
    approved_by = models.ForeignKey(Employees, on_delete=models.DO_NOTHING, null=True)
    url_name = models.CharField(max_length=100, default='')
    request_method = models.CharField(max_length=100, default='')
    payload = models.TextField(default='')
    approval_code = models.CharField(max_length=10, default='', unique=True)
    request_time = models.DateTimeField(auto_now_add=True)
    approved_time = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'approvals'

    def create(self, organisation_id: int, request_from: str, url_name: str, request_method: str,
               payload: str, organisation_name: str, approved_time: datetime.datetime = None,
               approved_by: int = None):
        self.organisation_id = Organisation(organisation_id=organisation_id)
        self.request_from = request_from
        self.approved_by = approved_by
        self.url_name = url_name
        self.request_method = request_method
        self.payload = payload
        self.approved_time = approved_time
        self.save()
        self.approval_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(self.approval_id)
        self.save()
        return self.approval_code

    @staticmethod
    def get_all_unapproved(organisation_name: str) -> list:
        return Approvals.objects.filter(organisation_id__company_name=organisation_name, approved_time__isnull=True).values(
            'request_from', 'request_method', 'payload', 'approval_code').order_by('approval_code')

    @staticmethod
    def get_by_code(approver_code: str, organisation_name: str) -> dict:
        return Approvals.objects.filter(approval_code=approver_code,
                                        organisation_id__company_name=organisation_name).values().first()
