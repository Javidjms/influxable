import requests
from urllib.parse import urljoin


class InfluxDBRequest(requests.Session):
    def __init__(self, base_url, database_name):
        super().__init__()
        self.base_url = base_url
        self.database_name = database_name

    def request(self, method, url, **kwargs):
        return super().request(method, urljoin(self.base_url, url), **kwargs)

    def head(self, url, **kwargs):
        return super().head(urljoin(self.base_url, url), **kwargs)

    def get(self, url, **kwargs):
        return super().get(urljoin(self.base_url, url), **kwargs)

    def post(self, url, **kwargs):
        return super().post(urljoin(self.base_url, url), **kwargs)

    def put(self, url, **kwargs):
        return super().put(urljoin(self.base_url, url), **kwargs)

    def patch(self, url, **kwargs):
        return super().patch(urljoin(self.base_url, url), **kwargs)

    def delete(self, url, **kwargs):
        return super().delete(urljoin(self.base_url, url), **kwargs)
