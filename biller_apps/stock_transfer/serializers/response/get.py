from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.stock_transfer.serializers.response.get_all import StockTransferDataSerializer


class StockTransferGetDataSerializer(APiResponseSerializer):
    data = StockTransferDataSerializer()
