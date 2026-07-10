from django_elasticsearch_dsl.search import Search

from biller.config import Configurations


class PlacesEsQuery:
    @staticmethod
    def search_pattern_start_with_query_country(request_keys: str, response_keys=["country"]) -> set:
        search = Search(index='country').source(response_keys).query('bool', must=[
            {'query_string': {'fields': response_keys, 'query': request_keys + '*', 'default_operator': 'AND'}}
        ])
        search = search[0:Configurations.search_count]
        response = search.execute()
        data = []
        for hit in response:
            data.append(hit.country)
        return set(data)

    @staticmethod
    def search_pattern_start_with_query_state(country: str, request_keys: str, response_keys=["states"]) -> set:
        request_keys = request_keys + '*'
        search = Search(index='states').source(response_keys).query('bool', must=[
            {'query_string': {'fields': response_keys, 'query': request_keys + '*', 'default_operator': 'AND'}},
            {'match_phrase': {'country': country}}
        ])
        search = search[0:Configurations.search_count]
        response = search.execute()
        data = []
        for hit in response:
            data.append(hit.states)
        return set(data)
