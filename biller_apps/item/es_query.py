from biller_apps.common.elastich_query import ElasticQuery


class ItemEsQuery:
    @staticmethod
    def search_pattern_start_with_query(organisation_id: int, request_keys: str,response_keys=None) -> list:
        """
            response_keys = ["name", "item_code"]

        """
        if response_keys is None:
            response_keys = ["name"]

        source_search_col = ["name"]
        es=ElasticQuery(organisation_id=organisation_id,source_search_col=source_search_col,response_keys=response_keys)
        response=es.general_search(index_name='items',search_keys=request_keys)
        data = []
        for hit in response:
            data.append(hit['name'])
        return data
