from rest_framework import serializers

from biller_apps.organisation.dataclasses.request.create import OrganisationRequest


class OrganisationRequestSerializer(serializers.Serializer):
    owner_name = serializers.CharField(max_length=100)
    owner_mobile = serializers.CharField(max_length=20)
    owner_alternate_mobile = serializers.CharField(max_length=20)
    owner_email = serializers.CharField(max_length=30)
    name = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=100)
    shop_count = serializers.IntegerField()
    employee_count = serializers.IntegerField()
    approval = serializers.BooleanField(default=False)
    plan = serializers.CharField(max_length=100)
    plan_expiry = serializers.DateField()

    def create(self, validated_data) -> OrganisationRequest:
        return OrganisationRequest(**validated_data)
