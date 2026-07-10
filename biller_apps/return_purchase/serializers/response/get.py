from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.return_purchase.serializers.response.get_all import ReturnPurchaseDataSerializer


class ReturnPurchaseGetDataSerializer(APiResponseSerializer):
    data = ReturnPurchaseDataSerializer()
