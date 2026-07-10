import math
from dataclasses import asdict

from biller_apps.common.elastich_query import ElasticQuery


class AppTemplateEsQuery:
    @staticmethod
    def search_pattern_start_with_query(organisation_id: int, request_keys: str, limit: int, page_num: int,
                                        response_keys=None) -> tuple:
        """
            response_keys = ['name', 'brand_code']
        """
        source_search_col = ['name']
        if response_keys is None:
            response_keys = ['name', 'brand_code']

        es = ElasticQuery(organisation_id=organisation_id, response_keys=response_keys,
                          source_search_col=source_search_col)
        response = es.general_search(index_name='brand', search_keys=request_keys)

        data = []
        total_count = len(response)
        total_pages = math.ceil(total_count / limit)
        response = response[(page_num - 1) * limit: page_num * limit]
        for hit in response:
            search_res = AppTemplateSearchPattern(name=hit.name, brandCode=hit.brand_code)
            data.append(asdict(search_res))
        return data, total_pages, total_count
