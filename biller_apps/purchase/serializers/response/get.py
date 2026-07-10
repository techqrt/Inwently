from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.purchase.serializers.response.get_all import PurchaseDataSerializer


class PurchaseGetDataSerializer(APiResponseSerializer):
    data = PurchaseDataSerializer()
