from biller_apps.common.elastich_query import ElasticQuery


class PurchaseEsQuery:
    @staticmethod
    def search_pattern_start_with_query(organisation_id: int, request_keys: str,response_keys=None) -> list:
        """
            response_keys = ['purchase_bill_number', 'supplier_name', 'item_name',
                             'buying_price', 'landing_cost', 'selling_price',
                             'tax', 'quantity', 'bill_amount', 'created_date_time']
        """

        source_search_col = ['purchase_bill_number']
        if response_keys is None:
            response_keys = ['purchase_bill_number']
        es = ElasticQuery(organisation_id=organisation_id, response_keys=response_keys,
                          source_search_col=source_search_col)
        response = es.general_search(index_name='purchase', search_keys=request_keys)
        data = []
        for hit in response:
            data.append(hit["purchase_bill_number"])
        return data
