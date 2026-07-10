from biller_apps.common.elastich_query import ElasticQuery


class StockTransfersEsQuery:
    @staticmethod
    def search_pattern_start_with_query(organisation_id: int, request_keys: str,response_keys=None) -> list:
        """
            response_keys = ['transfer_id', 'source_shop_id', 'destination_shop_id', 'item_id', 
                             'quantity', 'transfer_date_time', 'created_date_time', 'status', 
                             'organisation_id', 'remarks', 'requested_by', 'approved_by']
        """

        # Default columns to search
        source_search_col = ['transfer_code']
        if response_keys is None:
            response_keys = ['transfer_code']
        
        es = ElasticQuery(organisation_id=organisation_id, response_keys=response_keys,
                          source_search_col=source_search_col)
        response = es.general_search(index_name='stock_transfer', search_keys=request_keys)
        
        data = []
        for hit in response:
            data.append(hit["transfer_code"])
        
        return data
