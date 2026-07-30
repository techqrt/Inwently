from django.db import models
from django.db.models import Q
from django.utils import timezone
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.organisation.models import Organisation
from biller_apps.shops.models import Shops
from biller_apps.item.models.items import Items


class StockTransfer(models.Model):
    transfer_id = models.AutoField(primary_key=True)
    transfer_code = models.CharField(max_length=10, default='', unique=True)
    source_shop_id = models.ForeignKey(Shops, related_name='source_shop', on_delete=models.CASCADE)
    destination_shop_id = models.ForeignKey(Shops, related_name='destination_shop', on_delete=models.CASCADE)
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    transfer_date_time = models.DateTimeField(default=timezone.now)
    created_date_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default='Pending') 
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    remarks = models.TextField(default='', null=True, blank=True)
    requested_by = models.CharField(max_length=100, default='', null=True, blank=True)
    approved_by = models.CharField(max_length=100, default='', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'stock_transfer'

    def create(self, source_shop_id: int, destination_shop_id: int, item_id: int, quantity: int,
               organisation_id: int, organisation_name: str, remarks: str = '', requested_by: str = '') -> int:
        self.source_shop_id = Shops(source_shop_id)
        self.destination_shop_id = Shops(destination_shop_id)
        self.item_id = Items(item_id)
        self.quantity = quantity
        self.transfer_date_time = timezone.now()
        self.created_date_time = timezone.now()
        self.status = 'Pending'
        self.organisation_id = Organisation(organisation_id)
        self.remarks = remarks
        self.requested_by = requested_by
        self.save()
        self.transfer_code = ''.join([i[0] for i in organisation_name.split()]) + '_' + str(self.transfer_id)
        self.save()
        return self.transfer_id

    @staticmethod
    def update(transfer_id: int, status: str, approved_by: str = '', remarks: str = '') -> int:
        transfer = StockTransfer.objects.get(transfer_id=transfer_id)
        transfer.status = status
        transfer.approved_by = approved_by
        transfer.remarks = remarks
        transfer.save()
        return transfer.transfer_id

    @staticmethod
    def get(organisation_name: str, transfer_code: str) -> dict:
        return StockTransfer.objects.filter(
            transfer_code=transfer_code,
            organisation_id__company_name=organisation_name
        ).values(
            'transfer_id', 'source_shop_id__name', 'destination_shop_id__name',
            'item_id__name', 'quantity', 'status', 'transfer_date_time', 'remarks',
            'requested_by', 'approved_by'
        ).first()

    @staticmethod
    def get_pending_transfers(organisation_name: str) -> list:
        return StockTransfer.objects.filter(
            organisation_id__company_name=organisation_name, status='Pending'
        ).values(
            'transfer_id', 'source_shop_id__name', 'destination_shop_id__name',
            'item_id__name', 'quantity', 'transfer_date_time', 'requested_by'
        ).order_by('transfer_date_time')

    @staticmethod
    def get_completed_transfers(organisation_name: str) -> list:
        return StockTransfer.objects.filter(
            organisation_id__company_name=organisation_name, status='Completed'
        ).values(
            'transfer_id', 'source_shop_id__name', 'destination_shop_id__name',
            'item_id__name', 'quantity', 'transfer_date_time', 'requested_by'
        ).order_by('transfer_date_time')

    @staticmethod
    def get_rejected_transfers(organisation_name: str) -> list:
        return StockTransfer.objects.filter(
            organisation_id__company_name=organisation_name, status='Rejected'
        ).values(
            'transfer_id', 'source_shop_id__name', 'destination_shop_id__name',
            'item_id__name', 'quantity', 'transfer_date_time', 'requested_by'
        ).order_by('transfer_date_time')
    
    @staticmethod
    def get_all(organisation_name: str,params:GetAll) -> list:
        filters=Q(organisation_id__company_name=organisation_name)
        
        if params.filter_value and params.filter_key:
            if params.filter_key.lower() =='is_active':
                filters=filters & Q(is_active=params.filter_value.lower()=='true')
            else:
                filters=filters & Q(**{params.filter_key:params.filter_value})
            
        if len(params.search_key)>0:
                filters&=Q(transfer_code__icontains=params.search_key)
        if params.sort_by == 'name':
            params.sort_by = "transfer_date_time"
            params.ordering = f"{'-' if params.sort_order == 'desc' else ''}{params.sort_by}"
        return StockTransfer.objects.filter(filters).values(
            'transfer_id', 'source_shop_id__name', 'destination_shop_id__name',
            'item_id__name', 'quantity', 'status', 'transfer_date_time', 'remarks',
            'requested_by', 'approved_by'
        ).order_by(params.ordering)

    @staticmethod
    def remove(transfer_id: int):
        StockTransfer.objects.get(transfer_id=transfer_id).delete()

    @staticmethod
    def get_sorted_transfers(organisation_name: str, sort_order: str) -> list:
        order_by = 'transfer_date_time' if sort_order == 'asc' else '-transfer_date_time'
        return StockTransfer.objects.filter(
            organisation_id__company_name=organisation_name
        ).values(
            'transfer_id', 'source_shop_id__name', 'destination_shop_id__name',
            'item_id__name', 'quantity', 'status', 'transfer_date_time'
        ).order_by(order_by)
