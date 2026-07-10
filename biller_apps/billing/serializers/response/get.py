from biller_apps.billing.serializers.response.get_all import BillDataSerializer
from biller_apps.common.serializers.response.api_response import APiResponseSerializer


class BillDataGetResponseSerializer(APiResponseSerializer):
    data = BillDataSerializer()
