# biller_apps/pos/models.py
from django.db import models
from django.utils import timezone

from biller_apps.customer.models import Customer
from biller_apps.employees.models.employees import Employees
from biller_apps.item.models.items import Items
from biller_apps.organisation.models import Organisation
from biller_apps.shops.models import Shops


class POS(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_SENT_TO_CUSTOMER = 'sent_to_customer'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_EXECUTED = 'executed'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_SENT_TO_CUSTOMER, 'Sent to Customer'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_EXECUTED, 'Executed'),
    ]

    PAYMENT_PENDING = 'pending'
    PAYMENT_PAID = 'paid'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_PAID, 'Paid'),
    ]

    pos_id = models.AutoField(primary_key=True)
    pos_code = models.CharField(max_length=25, null=True, blank=True, unique=True)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    shop_id = models.ForeignKey(Shops, on_delete=models.CASCADE)
    billed_by = models.ForeignKey(Employees, on_delete=models.DO_NOTHING, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_quotation_id = models.IntegerField(null=True, blank=True, default=None)
    payment_type = models.CharField(max_length=15, default='')
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discounts_unit = models.CharField(
        max_length=20, default='percentage',
        choices=[('percentage', 'Percentage'), ('flat', 'Flat')],
    )
    wave_off = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'pos'


class POSItem(models.Model):
    pos_item_id = models.AutoField(primary_key=True)
    pos_id = models.ForeignKey(POS, on_delete=models.CASCADE, related_name='items')
    item_id = models.ForeignKey(Items, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'pos_item'