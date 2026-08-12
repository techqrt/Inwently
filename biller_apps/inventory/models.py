import datetime
import uuid
from django.db import models
from django.db.models import Q
from django.utils import timezone

from biller_apps.brand.models import Brand
from biller_apps.organisation.models import Organisation
from biller_apps.item.models.items import Items
from biller_apps.shops.models import Shops


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(Items, on_delete=models.DO_NOTHING)
    shop_id = models.ForeignKey(Shops, on_delete=models.DO_NOTHING)
    inventory_code = models.CharField(max_length=25, null=True, blank=True, unique=True)
    # Nullable: expiry_date is optional on create (not every item batch has one).
    expiry_date = models.DateField(null=True, blank=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_qty = models.PositiveIntegerField(default=0)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(default=timezone.now)
    store_mapping = models.CharField(max_length=100, default='', null=True, blank=True)

    class Meta:
        db_table = 'inventory'

    # NOTE: the old Inventory.get_all(organisation_name) staticmethod has been removed.
    # It was superseded by InventoryUtils.get_all(organisation_id, ...), which supports
    # pagination-friendly filtering/sorting by shop_code, item_code, and other fields.
    # If anything else in the codebase still calls Inventory.get_all(...), it will need
    # to be updated to use InventoryUtils.get_all(...) instead.

#InventoryLog model is used to log the changes made to the inventory table. It has a foreign key relationship with the Inventory model and stores information about the event type, status, and error message (if any) related to the change made to the inventory. The log_id field is an auto-incrementing primary key, and the batch_id field is a UUID that can be used to group related log entries together. The change_date field stores the timestamp of when the change was made. The model also defines choices for event types and status, which can be used to filter log entries based on these fields.    

class InventoryLog(models.Model):
    EVENT_CREATE = "CREATE"
    EVENT_UPDATE = "UPDATE"
    EVENT_BULK_CREATE = "BULK_CREATE"
    EVENT_BULK_UPDATE = "BULK_UPDATE"
    EVENT_CHOICES = [
        (EVENT_CREATE, "Create"),
        (EVENT_UPDATE, "Update"),
        (EVENT_BULK_CREATE, "Bulk Create"),
        (EVENT_BULK_UPDATE, "Bulk Update"),
    ]

    STATUS_SUCCESS = "SUCCESS"
    STATUS_FAILED = "FAILED"
    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAILED, "Failed"),
    ]

    log_id = models.AutoField(primary_key=True)
    inventory_id = models.ForeignKey(
        Inventory, on_delete=models.SET_NULL, null=True, blank=True
    )
    inventory_code = models.CharField(max_length=25, null=True, blank=True)
    change_date = models.DateTimeField(default=timezone.now)
    eventtype = models.CharField(max_length=20, choices=EVENT_CHOICES)
    batch_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_SUCCESS)
    error_message = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'inventory_logs'
        indexes = [
            models.Index(fields=["batch_id"]),
            models.Index(fields=["inventory_code"]),
        ]    