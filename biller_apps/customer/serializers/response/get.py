from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.customer.serializers.response.get_all import CustomerDataSerializer


class CustomerGetResponseSerializer(APiResponseSerializer):
    data = CustomerDataSerializer()
