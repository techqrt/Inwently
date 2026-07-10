from biller_apps.common.serializers.response.api_response import APiResponseSerializer
from biller_apps.organisation.serializers.response.get_all import OrganisationDataSerializer


class OrganisationGetResponseSerializer(APiResponseSerializer):
    data = OrganisationDataSerializer()
