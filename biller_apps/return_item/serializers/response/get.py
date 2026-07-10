from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.return_item.serializers.response.get_all import ReturnItemDataSerializer


class ReturnItemGetDataSerializer(APiResponseSerializer):
    data = ReturnItemDataSerializer()
