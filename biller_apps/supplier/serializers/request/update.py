from rest_framework import serializers

from biller_apps.supplier.dataclasses.request.update import SupplierUpdate


class SupplierUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=100)
    mobile_number = serializers.CharField(max_length=20)
    email_id = serializers.EmailField()
    supplier_code = serializers.CharField(max_length=10)
    id_number = serializers.CharField(max_length=100)
    id_type = serializers.CharField(max_length=100)
    gst_number = serializers.CharField(max_length=100)
    photo_url = serializers.CharField(allow_blank=True, allow_null=True, default=None)
    id_proof_url = serializers.CharField(allow_blank=True, allow_null=True, default=None)
    alt_mobile_number = serializers.CharField(max_length=20, allow_blank=True, allow_null=True, default=None)

    def create(self, validated_data) -> SupplierUpdate:
        return SupplierUpdate(**validated_data)
