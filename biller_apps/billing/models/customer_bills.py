from django.db import models

from django.utils import timezone

from biller_apps.employees.models.employees import Employees

from biller_apps.organisation.models import Organisation
from biller_apps.shops.models import Shops


class CustomerBills(models.Model):
    customer_bills_id = models.AutoField(primary_key=True)
    bill_number = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(default=timezone.now)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    billed_by = models.ForeignKey(Employees, on_delete=models.DO_NOTHING)
    shop_id = models.ForeignKey(Shops, on_delete=models.CASCADE)
    discounts = models.FloatField(default=0)
    discounts_unit = models.CharField(max_length=20, default='percentage')
    wave_off = models.FloatField(default=0)

    class Meta:
        db_table = 'customer_bills'