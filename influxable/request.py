import requests
from urllib.parse import urljoin


class InfluxDBRequest(requests.Session):
    def __init__(self, base_url, database_name, auth):
        super().__init__()
        self.base_url = base_url
        self.database_name = database_name
        self.auth = auth

    def request(self, method, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().request(method, url=full_url, **kwargs)

    def head(self, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().head(full_url, **kwargs)

    def get(self, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().get(full_url, **kwargs)

    def post(self, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().post(full_url, **kwargs)

    def put(self, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().put(full_url, **kwargs)

    def patch(self, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().patch(full_url, **kwargs)

    def delete(self, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().delete(full_url, **kwargs)
