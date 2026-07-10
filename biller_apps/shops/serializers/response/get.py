from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.shops.serializers.response.get_all import ShopGetAllDataSerializer


class ShopGetRequestSerializer(APiResponseSerializer):
    data = ShopGetAllDataSerializer()
