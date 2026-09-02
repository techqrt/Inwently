from rest_framework import serializers

from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.common.serializers.response.get_all import GetAllGeneralSerializer


class PermissionsMasterSerializer(serializers.Serializer):
    item = serializers.BooleanField()
    shop = serializers.BooleanField()
    supplier = serializers.BooleanField()
    customer = serializers.BooleanField()
    create = serializers.BooleanField()
    employee = serializers.BooleanField()


class PermissionsInventorySerializer(serializers.Serializer):
    inventory = serializers.BooleanField()


class PermissionsBillingSerializer(serializers.Serializer):
    billHistory = serializers.BooleanField()
    pos = serializers.BooleanField()
    returnItem = serializers.BooleanField()


class PermissionsReportsSerializer(serializers.Serializer):
    overview = serializers.BooleanField()
    general = serializers.BooleanField()
    administration = serializers.BooleanField()
    dayBook = serializers.BooleanField()
    gst = serializers.BooleanField()


class PermissionsDashboardSerializer(serializers.Serializer):
    dashboard = serializers.BooleanField()


class PermissionsStockSerializer(serializers.Serializer):
    stock = serializers.BooleanField()
    purchaseList = serializers.BooleanField()
    returnPurchase = serializers.BooleanField()

class PermissionsQuotationsSerializer(serializers.Serializer):
    quotations = serializers.BooleanField()

class PermissionsDispatchSerializer(serializers.Serializer):
    dispatch = serializers.BooleanField()

class PermissionsPrinterTemplatesSerializer(serializers.Serializer):
    printerTemplates = serializers.BooleanField()

class PermissionsSerializer(serializers.Serializer):
    master = PermissionsMasterSerializer()
    inventory = PermissionsInventorySerializer()
    billing = PermissionsBillingSerializer()
    reports = PermissionsReportsSerializer()
    printerTemplates = PermissionsPrinterTemplatesSerializer()
    dashboard = PermissionsDashboardSerializer()
    stock = PermissionsStockSerializer()
    quotations = PermissionsQuotationsSerializer()
    dispatch = PermissionsDispatchSerializer()


class EmployeesDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    mobileNumber = serializers.CharField(required=False, allow_blank=True)
    alternatemobilenumber = serializers.CharField(required=False, allow_blank=True)
    dob = serializers.DateField(input_formats=['%Y-%m-%d'])
    state = serializers.CharField()
    country = serializers.CharField()
    street = serializers.CharField()
    organisationName = serializers.CharField()
    isActive = serializers.BooleanField()
    emailId = serializers.EmailField()
    emailVerified = serializers.BooleanField()
    profilePhotoUrl = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    employeeCode = serializers.CharField()
    permissions = PermissionsSerializer()


class EmployeesGetAllSerializer(GetAllGeneralSerializer):
    data = serializers.ListField(child=EmployeesDataSerializer())


class EmployeesGetAllResponseSerializer(APiResponseSerializer):
    data = EmployeesGetAllSerializer()
