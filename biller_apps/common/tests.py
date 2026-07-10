# import pytest
# from django.http import HttpRequest
# from rest_framework.request import Request
#
# from biller_apps.common.utils import Utils
#
#
# class TestUtils:
#     @pytest.fixture
#     def ins_util(self):
#         return Utils()
#
#     def test_success_response_data_with_message_and_data(self, ins_util):
#         response = ins_util.success_response_data('success', {'key': 'value'})
#         assert response == {'status': True, 'message': 'success', 'data': {'key': 'value'}}
#
#     def test_success_response_data_with_only_message(self, ins_util):
#         response = ins_util.success_response_data(message='success')
#         assert response == {'status': True, 'message': 'success'}
#
#     def test_error_response_data_with_message_and_error(self, ins_util):
#         response = ins_util.error_response_data('error', ['error1', 'error2'])
#         assert response == {'status': False, 'message': 'error', 'error': ['error1', 'error2']}
#
#     def test_get_query_params(self, ins_util):
#         _request = HttpRequest()
#         _request.path = 'http://127.0.0.1:8050/supplier/get/?name=joseph'
#         _request.content_type = 'application/json'
#         _request.method = 'GET'
#         _request.content_type = 'application/json'
#         request = Request(_request)
#         request.body = {}
#         response = ins_util.get_query_params(request)
#         assert response == {'name': 'joseph'}
#
#     def test_add_page_parameter(self, ins_util):
#         response = ins_util.add_page_parameter([], 1, present_url='http://localhost:8000/')
#         assert response == {'data': [], 'next_page_url': 'http://localhost:8000/?page_num=2'}
#
#     def test_add_page_parameter_future_page(self, ins_util):
#         response = ins_util.add_page_parameter([], 1, present_url='http://localhost:8000/?page_num=1')
#         assert response == {'data': [], 'next_page_url': 'http://localhost:8000/?page_num=2'}
