# biller_apps/customer_quotation/models.py
from django.db import models # type: ignore
from django.utils import timezone #type: ignore

from biller_apps.organisation.models import Organisation
from biller_apps.shops.models import Shops
from biller_apps.item.models.items import Items
from biller_apps.employees.models.employees import Employees


class CustomerQuotation(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PHONE_CONFIRMED = 'phone_confirmed'
    STATUS_REJECTED = 'rejected'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CONVERTED = 'converted'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PHONE_CONFIRMED, 'Phone Confirmed'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_CONVERTED, 'Converted'),
    ]

    customer_quotation_id = models.AutoField(primary_key=True)
    customer_quotation_code = models.CharField(max_length=25, null=True, blank=True, unique=True)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    shop_id = models.ForeignKey(Shops, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.CharField(max_length=120, blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reviewed_by = models.ForeignKey(Employees, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'customer_quotation'


class CustomerQuotationItem(models.Model):
    customer_quotation_item_id = models.AutoField(primary_key=True)
    customer_quotation_id = models.ForeignKey(
        CustomerQuotation, on_delete=models.CASCADE, related_name='items'
    )
    item_id = models.ForeignKey(Items, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'customer_quotation_item'