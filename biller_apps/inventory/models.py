import datetime
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