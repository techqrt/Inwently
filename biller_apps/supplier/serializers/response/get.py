from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.supplier.serializers.response.get_all import SuppliersDataSerializer


class SupplierGetDataSerializer(APiResponseSerializer):
    data = SuppliersDataSerializer()
