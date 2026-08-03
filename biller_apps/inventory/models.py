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
    expiry_date = models.DateField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_qty = models.PositiveIntegerField(default=0)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'inventory'

    @staticmethod 
    def get_all(organisation_name: str) -> list:
        return Inventory.objects.filter(
            organisation_id__company_name=organisation_name
        ).values(
            'item_id__item_code', 'item_id__name', 'item_id__description', 'shop_id__name', 'shop_id__shop_code',
            'item_id__brand_id__name', 'expiry_date', 'price', 'balance_qty', 'created_time',
        ).order_by('-created_time')
