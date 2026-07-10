import json

import requests
from rest_framework import status
from rest_framework.response import Response

from biller.config import Configurations
from biller_apps.common.utils import Utils


class SocketApis:
    def __init__(self, success_msg: str, error_message: str):
        self.host = Configurations.socket_apis['host']
        self.port = Configurations.socket_apis['port']
        self.success_msg = success_msg
        self.error_message = error_message

    @staticmethod
    def check_socket_server(func):
        def check(*args, **kwargs):
            if Configurations.socket_server_connect['enable']:
                result = func(*args, **kwargs)
                return result
            return 'socket server is not enabled'

        return check

    @check_socket_server
    def socket_response(self, address: tuple, message: str) -> bool:
        try:
            url = self.host + ':' + str(self.port) + '/socket_response'
            data = {
                "address": address,
                "message": message
            }
            headers = {'content-type': 'application/json'}
            requests.post(url=url, data=json.dumps(data), headers=headers)
            return True
        except Exception as e:
            return False

    def socket_call(self, func):
        def task(*args, **kwargs):
            try:
                body = json.loads(args[1].body)
            except:
                body = Utils.get_query_params(args[1])
                if 'callback_url' in body.keys():
                    call_back = body['callback_url'].split(',')
                    body['callback_url'] = [call_back[0], int(call_back[1])]

            try:
                res = func(*args, **kwargs)
                if 'callback_url' in body.keys():
                    self.socket_response(address=tuple(body['callback_url']), message=self.success_msg)
                return res
            except Exception as e:
                if 'callback_url' in body.keys():
                    self.socket_response(address=tuple(body['callback_url']), message=str(e))
                return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))

        return task
