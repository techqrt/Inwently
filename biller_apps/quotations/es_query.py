from biller_apps.common.elastich_query import ElasticQuery


class QuotationEsQuery:
    @staticmethod
    def search_pattern_start_with_query(organisation_id: int, request_keys: str,response_keys=None) -> list:
        """
            response_keys = ['quotation_code', 'supplier_name', 'item_name', 'description',
                             'brand', 'quantity', 'price', 'tax', 'total', 'created_date']
        """

        source_search_col = ['quotation_code']
        if response_keys is None:
            response_keys = ['quotation_code']
        es = ElasticQuery(organisation_id=organisation_id, response_keys=response_keys,
                          source_search_col=source_search_col)
        response = es.general_search(index_name='quotation', search_keys=request_keys)
        data = []

        for hit in response:
            data.append(hit["quotation_code"])
        return data
