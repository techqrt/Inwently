
from django.db import models

from biller_apps.purchase.models.purchase import Purchase
from biller_apps.shops.models import Shops


class BranchSplit(models.Model):
    branch_split_id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Shops, on_delete=models.DO_NOTHING)
    quantity = models.FloatField(default=0.0)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)

    class Meta:
        db_table = 'branch_split'

    def create(self,shop:str,quantity:float,purchase:int):
        self.shop = Shops.objects.filter(shop_code=shop).first()
        self.quantity = quantity
        self.purchase = Purchase(purchase_id=purchase)
        self.save()
        return self.branch_split_id

