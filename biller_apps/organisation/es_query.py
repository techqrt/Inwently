from biller_apps.common.elastich_query import ElasticQuery


class OrganisationEsQuery:
    @staticmethod
    def search_pattern_start_with_query(organisation_id: int, request_keys: str,response_keys=None) -> list:
        """
            response_keys = ['company_name', 'owner_name', 'owner_mobile', 'owner_alternate_mobile', 
                             'owner_email', 'created_date_time', 'shop_count', 'employee_count', 
                             'approval', 'plan', 'plan_expiry', 'payment_gateway', 'image']
        """

        source_search_col = ['company_name']
        if response_keys is None:
            response_keys = ['company_name']
        es = ElasticQuery( response_keys=response_keys,
                          source_search_col=source_search_col)
        response = es.general_search(index_name='organisation', search_keys=request_keys)
        data = []
        for hit in response:
            data.append(hit['comapny_name'])
        return data
