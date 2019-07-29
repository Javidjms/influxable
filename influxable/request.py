import requests
from urllib.parse import urljoin


class InfluxDBRequest(requests.Session):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, **kwargs):
        return super().request(method, urljoin(self.base_url, url), **kwargs)
