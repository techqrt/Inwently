from rest_framework import status
from rest_framework.response import Response

from biller_apps.common.common import Common
from biller_apps.common.utils import Utils
from biller_apps.places.es_query import PlacesEsQuery
from biller_apps.places.models.country import Country
from biller_apps.places.models.states import States
from biller_apps.places.serializers.request.get import PlacesGet


class PlaceView:
    def __init__(self) -> None:
        self.fetch_data = "Data fetched successfully"
        self.delete_data = "Place delete successfully"
        self.update_data = "Place updated successfully"
        self.created_data = "Place added successfully"
        super().__init__()

    @staticmethod
    def country_data_prepare(countries: list) -> list:
        return [country['country'] for country in countries]

    @staticmethod
    def states_data_prepare(states: list) -> list:
        return [state['states'] for state in states]

    @Common().exception_handler
    def get_extract(self, params: PlacesGet):
        data = []
        if params.country is None and params.state is None:
            country = Country.get_country()
            data = self.country_data_prepare(countries=country)
        elif params.country is not None and params.state is None:
            data = PlacesEsQuery.search_pattern_start_with_query_country(request_keys=params.country)
            if params.country_selection is False:
                states = States.get_states(country=params.country)
                data = self.states_data_prepare(states=states)
        elif params.country is not None and params.state is not None:
            data = PlacesEsQuery.search_pattern_start_with_query_state(country=params.country,
                                                                       request_keys=params.state)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.fetch_data, data=data))
