from rest_framework import serializers

from biller_apps.billing.dataclasses.request.create import BillingRequest
from biller_apps.employees.models.employees import Employees

class BillingRequestSerializer(serializers.Serializer):
    items = serializers.ListField(default=[{'item_code': None, 'quantity': None}])

    def create(self, validated_data) -> BillingRequest:
        token_payload = self.context['request'].payload
        employee = Employees.get_with_email(email_id=token_payload.email_id)

        return BillingRequest(
            billed_by=employee['employee_code'],
            shop_code=employee['shop_access'][0]['shopCode'],
            items=validated_data['items']
        ) 