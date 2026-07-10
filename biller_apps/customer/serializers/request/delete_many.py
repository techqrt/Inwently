from rest_framework import serializers

from biller_apps.customer.dataclasses.request.delete_many import CustomerDeleteManyRequest


class CustomerDeleteManySerializer(serializers.Serializer):
    customer_code = serializers.ListField(required=True)

    def create(self, validated_data) -> CustomerDeleteManyRequest:
        return CustomerDeleteManyRequest(**validated_data)
