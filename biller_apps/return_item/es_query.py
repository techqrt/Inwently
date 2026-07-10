from biller_apps.common.elastich_query import ElasticQuery


class ReturnItemEsQuery:
    @staticmethod
    def search_pattern_start_with_query(organisation_id: int, request_keys: str,response_keys=None) -> list:

        source_search_col = ['return_code']
        if response_keys is None:
            response_keys = ['return_code']
        es = ElasticQuery(organisation_id=organisation_id, response_keys=response_keys,
                          source_search_col=source_search_col)
        response = es.general_search(index_name='return_item', search_keys=request_keys)
        data = []
        for hit in response:
            data.append(hit["return_code"])
        return data
