from rest_framework import serializers

from biller_apps.employees.dataclasses.request.create import EmployeesRequest


class PermissionsRequestMasterSerializer(serializers.Serializer):
    item = serializers.BooleanField()
    shop = serializers.BooleanField()
    supplier = serializers.BooleanField()
    customer = serializers.BooleanField()
    create = serializers.BooleanField()
    employee = serializers.BooleanField()


class PermissionsRequestInventorySerializer(serializers.Serializer):
    inventory = serializers.BooleanField()


class PermissionsRequestBillingSerializer(serializers.Serializer):
    bill_history = serializers.BooleanField()
    pos = serializers.BooleanField()
    return_item = serializers.BooleanField()


class PermissionsRequestReportsSerializer(serializers.Serializer):
    overview = serializers.BooleanField()
    general = serializers.BooleanField()
    administration = serializers.BooleanField()
    day_book = serializers.BooleanField()
    gst = serializers.BooleanField()


class PermissionsRequestDashboardSerializer(serializers.Serializer):
    dashboard = serializers.BooleanField()


class PermissionsRequestStockSerializer(serializers.Serializer):
    stock = serializers.BooleanField()
    purchase_list = serializers.BooleanField()
    return_purchase = serializers.BooleanField()


class PermissionsRequestQuotationsSerializer(serializers.Serializer):
    quotations = serializers.BooleanField()


class PermissionsRequestDispatchSerializer(serializers.Serializer):
    dispatch = serializers.BooleanField()


class PermissionsRequestPrinterTemplatesSerializer(serializers.Serializer):
    printer_templates = serializers.BooleanField()


class PermissionsRequestSerializer(serializers.Serializer):
    master = PermissionsRequestMasterSerializer()
    inventory = PermissionsRequestInventorySerializer()
    billing = PermissionsRequestBillingSerializer()
    reports = PermissionsRequestReportsSerializer()
    printer_templates = PermissionsRequestPrinterTemplatesSerializer()
    dashboard = PermissionsRequestDashboardSerializer()
    stock = PermissionsRequestStockSerializer()
    quotations = PermissionsRequestQuotationsSerializer()
    dispatch = PermissionsRequestDispatchSerializer()


class EmployeesRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    mobile_number = serializers.CharField(max_length=20)
    alternate_mobile_number = serializers.CharField(max_length=20,required=False,default=None,allow_null=True,allow_blank=True)
    dob = serializers.DateField()
    shop_access = serializers.ListField()
    email_id = serializers.EmailField()
    state = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=100)
    profile_photo_url = serializers.CharField(default=None, allow_blank=True, allow_null=True)
    permissions = PermissionsRequestSerializer()

    def create(self, validated_data) -> EmployeesRequest:
        return EmployeesRequest(**validated_data)
