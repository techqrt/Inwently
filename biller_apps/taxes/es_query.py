from biller_apps.common.elastich_query import ElasticQuery


class TaxesEsQuery:
    @staticmethod
    def search_pattern_start_with_query(organisation_id: int, request_keys: str,response_keys=None) -> list:
        """
            response_keys = ['name', 'tax_code', 'total_tax']
        """

        source_search_col = ['name']
        if response_keys is None:
            response_keys = ['name']

        es = ElasticQuery(organisation_id=organisation_id, response_keys=response_keys,
                          source_search_col=source_search_col)
        response = es.general_search(index_name='taxes', search_keys=request_keys)
        data = []

        for hit in response:
            data.append(hit['name'])
        return data
