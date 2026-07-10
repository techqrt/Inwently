from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.item.serializers.response.get_all import ItemGetAllSerializer


class ItemGetResponseSerializer(APiResponseSerializer):
    data = ItemGetAllSerializer()
