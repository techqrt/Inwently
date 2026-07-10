from rest_framework import serializers

from biller_apps.supplier.dataclasses.request.create import SupplierRequest


class SupplierRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=100)
    mobile_number = serializers.CharField(max_length=20)
    alt_mobile_number = serializers.CharField(max_length=20, required=False, default=None, allow_null=True,
                                              allow_blank=True)
    email_id = serializers.EmailField()
    id_number = serializers.CharField(max_length=100)
    id_type = serializers.CharField(max_length=100)
    gst_number = serializers.CharField(max_length=100)
    photo_url = serializers.CharField(allow_blank=True, allow_null=True, default=None)
    id_proof_url = serializers.CharField(allow_blank=True, allow_null=True, default=None)

    def create(self, validated_data) -> SupplierRequest:
        return SupplierRequest(**validated_data)
