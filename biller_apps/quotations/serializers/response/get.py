from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.quotations.serializers.response.get_all import QuotationDataSerializer


class QuotationGetDataSerializer(APiResponseSerializer):
    data = QuotationDataSerializer()