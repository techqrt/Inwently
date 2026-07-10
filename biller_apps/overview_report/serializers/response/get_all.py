from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class ItemOverviewReportDataSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=500, allow_blank=True, allow_null=True)
    code = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()
    item_code = serializers.CharField(max_length=100)
    created_time = serializers.DateTimeField()
    image_url = serializers.CharField(max_length=350, allow_blank=True, allow_null=True)
    brand_name = serializers.CharField(source='brand_id__name', max_length=255, allow_blank=True, allow_null=True)
    brand_code = serializers.CharField(source='brand_id__brand_code', max_length=100, allow_blank=True, allow_null=True)
    supplier_name = serializers.CharField(source='supplier_id__name', max_length=255, allow_blank=True, allow_null=True)
    supplier_code = serializers.CharField(source='supplier_id__supplier_code', max_length=100, allow_blank=True, allow_null=True)
    category_name = serializers.CharField(source='category_id__name', max_length=255, allow_blank=True, allow_null=True)
    category_code = serializers.CharField(source='category_id__category_code', max_length=100, allow_blank=True, allow_null=True)


class ItemOverviewReportGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=ItemOverviewReportDataSerializer())


class ItemOverviewReportDataSerializer(APiResponseSerializer):
    data = ItemOverviewReportGetAllSerializer()


class CustomerOverviewReportDataSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    mobile_number = serializers.CharField(max_length=20)
    email_id = serializers.EmailField(allow_null=True)
    customer_code = serializers.CharField(max_length=10)
    date_of_birth = serializers.DateField(allow_null=True)
    gender = serializers.CharField(max_length=1, allow_null=True)
    martial_status = serializers.CharField(max_length=100, allow_null=True)
    religion = serializers.CharField(max_length=100, allow_null=True)
    blood_group = serializers.CharField(max_length=100, allow_null=True)
    education = serializers.CharField(max_length=100, allow_null=True)
    occupation = serializers.CharField(max_length=100, allow_null=True)
    is_active = serializers.BooleanField()
    created_date_time = serializers.DateTimeField()
    photo_url = serializers.CharField(max_length=350, allow_null=True)
    id_proof_url = serializers.CharField(max_length=350, allow_null=True)


class CustomerOverviewReportGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=CustomerOverviewReportDataSerializer())


class CustomerOverviewReportDataSerializer(APiResponseSerializer):
    data = CustomerOverviewReportGetAllSerializer()


class SupplierOverviewReportDataSerializer(serializers.Serializer):
    supplier_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    mobile_number = serializers.CharField(max_length=20)
    email_id = serializers.EmailField()
    supplier_code = serializers.CharField(max_length=10)
    gst_number = serializers.CharField(max_length=100)
    id_number = serializers.CharField(max_length=100)
    id_type = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()
    created_date_time = serializers.DateTimeField()
    photo_url = serializers.CharField(max_length=350, allow_null=True)
    id_proof_url = serializers.CharField(max_length=350, allow_null=True)


class SupplierOverviewReportGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=SupplierOverviewReportDataSerializer())


class SupplierOverviewReportDataSerializer(APiResponseSerializer):
    data = SupplierOverviewReportGetAllSerializer()
