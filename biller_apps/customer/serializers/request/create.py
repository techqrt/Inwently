from rest_framework import serializers

from biller_apps.customer.dataclasses.request.create import CustomerRequest


class CustomerRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100, default=None, required=False,allow_null = True)
    country = serializers.CharField(max_length=100, default=None, required=False,allow_null = True)
    street = serializers.CharField(max_length=100, default=None, required=False,allow_null = True)
    mobile_number = serializers.CharField(max_length=20)
    email_id = serializers.EmailField(default=None, required=False,allow_null = True)
    id_number = serializers.CharField(max_length=100, default=None, required=False,allow_null = True)
    id_type = serializers.CharField(max_length=100, default=None, required=False,allow_null = True)
    photo_url = serializers.CharField(max_length=350, default=None, required=False,allow_null = True)
    id_proof_url = serializers.CharField(max_length=350, default=None, required=False,allow_null = True)
    occupation = serializers.CharField(max_length=100, default=None, required=False,allow_null = True)
    date_of_birth = serializers.DateField(default=None, required=False,allow_null = True)
    gender = serializers.CharField(max_length=1, default=None, required=False,allow_null = True)
    martial_status = serializers.CharField(max_length=100, default=None, required=False,allow_null = True)
    religion = serializers.CharField(max_length=100, default=None, required=False,allow_null = True)
    blood_group = serializers.CharField(max_length=100, default=None, required=False,allow_null = True)
    education = serializers.CharField(max_length=100, default=None, required=False,allow_null = True)

    def create(self, validated_data) -> CustomerRequest:
        return CustomerRequest(**validated_data)
