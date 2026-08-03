from django.db import models
from biller_apps.organisation.models import Organisation
from biller_apps.purchase.models.purchase import Purchase
from biller_apps.quotations.models import Quotation



class GeneralReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    purchase_id = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True, blank=True)
    quotation_id = models.ForeignKey(Quotation, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'general_report'

    @staticmethod
    def get_purchase_reports(organisation_name: str, start_date: str, end_date: str) -> list:
        return Purchase.objects.filter(
            purchase_bill__organisation_id__company_name=organisation_name,
            purchase_bill__created_date_time__range=[start_date, end_date]
        ).values(
            "purchase_id",
        "item__name",
        "purchase_bill__supplier__name",
        "quantity",
        "buying_price",
        "landing_cost",
        "selling_price",
        "tax",
        "purchase_bill__bill_amount",
        "purchase_bill__purchase_bill_number",
        "purchase_bill__purchase_code",
        "purchase_bill__created_date_time",
        ).order_by('-purchase_bill__created_date_time')

    @staticmethod
    def get_quotation_reports(organisation_name: str, start_date: str, end_date: str) -> list:
        return Quotation.objects.filter(
            organisation_id__company_name=organisation_name,  
            created_date__range=[start_date, end_date]  
        ).values(
            'quotation_id', 'quotation_code', 'supplier__name', 
            'created_date', 'total_amount', 'item__name',
            'description', 'brand', 'quantity',
            'price', 'tax', 'total',
            'purchase', 'sales'
        ).order_by('-created_date') 
