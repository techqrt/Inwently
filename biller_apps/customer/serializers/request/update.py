from rest_framework import serializers

from biller_apps.customer.dataclasses.request.update import CustomerUpdateRequest


class CustomerUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    customer_code = serializers.CharField(max_length=10)
    state = serializers.CharField(max_length=100, default=None, required=False)
    country = serializers.CharField(max_length=100, default=None, required=False)
    street = serializers.CharField(max_length=100, default=None, required=False)
    mobile_number = serializers.CharField(max_length=20)
    email_id = serializers.EmailField(default=None, required=False)
    id_number = serializers.CharField(max_length=100, default=None, required=False)
    id_type = serializers.CharField(max_length=100, default=None, required=False)
    photo_url = serializers.CharField(max_length=100, default=None, required=False)
    id_proof_url = serializers.CharField(max_length=100, default=None, required=False)
    occupation = serializers.CharField(max_length=100, default=None, required=False)
    date_of_birth = serializers.DateField(default=None, required=False)
    gender = serializers.CharField(max_length=1, default=None, required=False)
    martial_status = serializers.CharField(max_length=10, default=None, required=False)
    religion = serializers.CharField(max_length=100, default=None, required=False)
    blood_group = serializers.CharField(max_length=100, default=None, required=False)
    education = serializers.CharField(max_length=100, default=None, required=False)

    def create(self, validated_data) -> CustomerUpdateRequest:
        return CustomerUpdateRequest(**validated_data)
