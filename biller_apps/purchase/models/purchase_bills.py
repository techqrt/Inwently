from django.db import models
from django.utils import timezone


from biller_apps.supplier.models import Supplier

from biller_apps.organisation.models import Organisation


class PurchaseBills(models.Model):
    purchase_bill_id = models.AutoField(primary_key=True)
    purchase_code = models.CharField(max_length=10, default='', unique=True)
    purchase_bill_number = models.CharField(max_length=100, default='')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    bill_amount = models.FloatField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'purchase_bills'


    def create(self,purchase_bill_number:str,supplier_id:str,organisation_id:int,bill_amount:float,organisation_name:str):
        self.purchase_bill_number = purchase_bill_number
        self.supplier = Supplier.objects.filter(supplier_code=supplier_id).first()
        self.organisation_id = Organisation(organisation_id=organisation_id)
        self.bill_amount = bill_amount
        self.created_date_time = timezone.now()
        self.save()
        purchase_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(self.purchase_bill_id)
        self.purchase_code = purchase_code
        self.save()
        return self.purchase_bill_id