from django_elasticsearch_dsl.search import Search
from elasticsearch_dsl.query import Q
from biller.config import Configurations
from biller_apps.common.app_logger import Logger

class ElasticQuery:
    def __init__(self, response_keys: list, source_search_col: list, organisation_id: int=None):
        self.response_keys = response_keys  # Fields to return
        self.source_search_col = source_search_col  # Fields to search
        self.organisation_id = organisation_id  # Organisation filter

    def general_search(self, index_name: str, search_keys: dict):
        base_query = Q("match_all")  # Default: fetch first 10 records

        if search_keys:
            should_queries = []
            for field in self.source_search_col:
                should_queries.append(Q("match", **{field: search_keys}))  # Boost exact match
                should_queries.append(Q("prefix", **{field: search_keys}))  # Partial match

            base_query = Q("bool", should=should_queries, minimum_should_match=1)   

        if self.organisation_id:
            if index_name != "organisation":
                base_query = Q("bool", must=[Q("term", organisation_id_id=self.organisation_id)], should=[base_query],
                               minimum_should_match=1)
            else:
                base_query = Q("bool", should=[base_query], minimum_should_match=1)
                
        search = Search(index=index_name).source(self.response_keys).query(base_query)
        search = search[0:Configurations.search_count]
        try:
            return search.execute()
        except Exception as e:
            # Elasticsearch isn't configured/reachable in this environment -
            # degrade to no results instead of failing the whole request.
            Logger.log.warning('Elasticsearch unavailable, returning empty search result: ' + str(e))
            raise
            #return []
