from django.utils import timezone
from rest_framework import serializers

from biller_apps.purchase.dataclasses.request.create import PurchaseRequestDataclass


class BranchSplitSerializer(serializers.Serializer):
    branch_code = serializers.CharField()
    quantity = serializers.FloatField()

class PurchaseRequestSerializer(serializers.Serializer):
    UNIT_CHOICES = [
        ('Litre', 'Litre'),
        ('Count', 'Count'),
        ('Packet', 'Packet'),
        ('Box', 'Box'),
        ('Dozen', 'Dozen'),
        ('Pair', 'Pair'),
        ('Set', 'Set'),
        ('Meter', 'Meter'),
        ('Roll', 'Roll'),
        ('Piece', 'Piece'),
        ('Bag', 'Bag'),
        ('Unit', 'Unit'),
        ('Gram', 'Gram'),
        ('Kilogram', 'Kilogram'),
        ('Milligram','Milligram'),
        ('Ton','Ton')
    ]

    item_code = serializers.CharField(required=True)
    buying_price = serializers.FloatField(required=True)
    landing_cost = serializers.FloatField(default=0.0)
    selling_price = serializers.FloatField(required=True)
    tax = serializers.FloatField(default=0.0)
    quantity = serializers.FloatField(default=1)
    unit = serializers.ChoiceField(choices=UNIT_CHOICES,default="Unit")
    expiry = serializers.DateTimeField(default=timezone.now())
    branch_split = serializers.ListSerializer(child=BranchSplitSerializer())
    
class PurchaseSerializer(serializers.Serializer):
    purchase_bill_number = serializers.CharField()
    supplier_code = serializers.CharField()
    items = serializers.ListSerializer(child=PurchaseRequestSerializer())
    bill_amount = serializers.FloatField()

    def create(self, validated_data) -> PurchaseRequestDataclass:
        return PurchaseRequestDataclass(**validated_data)