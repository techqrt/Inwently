from rest_framework import serializers

from biller_apps.billing.dataclasses.request.create import BillingRequest
from biller_apps.employees.models.employees import Employees
from biller_apps.pos.dataclasses.request.update import POSItemAddEntry
from biller_apps.pos.serializers.request.update import POSItemAddEntrySerializer
from biller_apps.shops.models import Shops


class BillingRequestSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=120)
    customer_phone = serializers.CharField(max_length=20)
    items = POSItemAddEntrySerializer(many=True)

    def create(self, validated_data) -> BillingRequest:
        token_payload = self.context['request'].payload
        employee = Employees.get_with_email(email_id=token_payload.email_id)
        items = [POSItemAddEntry(**item) for item in validated_data['items']]

        # employee['shop_access'] is a plain list of shop_id ints (see
        # EmployeeUtils.get_shop_ids) — resolve the employee's first assigned
        # shop the same way, rather than assuming a {shopCode: ...} dict shape.
        shop = Shops.objects.filter(shop_id=employee['shop_access'][0]).first()
        if not shop:
            raise ValueError("Employee has no valid shop assigned.")

        return BillingRequest(
            customer_name=validated_data['customer_name'],
            customer_phone=validated_data['customer_phone'],
            billed_by=employee['employee_code'],
            shop_code=shop.shop_code,
            items=items,
        )
