import requests
from django.urls import reverse
from requests import Response

from biller_apps.auth.dataclasses.request.token_payload import Payload


class ReverseCall:
    def __init__(self, url_name: str, data: dict, payload: Payload):
        self.url_name = url_name
        self.data = data
        self.payload = payload
        self.base_url = self.get_base()
        self.header = {'Authorization': 'Bearer ' + self.payload.access_token}
        self.full_url = self.base_url + reverse(self.url_name)

    def get_base(self):
        split = self.payload.present_url.split('://')
        return split[0] + '://' + split[1].split('/')[0]

    def delete(self) -> Response:
        return requests.delete(self.full_url, params=self.data, headers=self.header)
