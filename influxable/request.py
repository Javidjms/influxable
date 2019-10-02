import requests
from urllib.parse import urljoin
from .decorators import raise_if_error


class InfluxDBRequest(requests.Session):
    def __init__(self, base_url, database_name, auth):
        super().__init__()
        self.base_url = base_url
        self.database_name = database_name
        self.auth = auth

    @raise_if_error
    def request(self, method, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().request(method, url=full_url, **kwargs)

    @raise_if_error
    def head(self, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().head(full_url, **kwargs)

    @raise_if_error
    def get(self, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().get(full_url, **kwargs)

    @raise_if_error
    def post(self, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().post(full_url, **kwargs)

    @raise_if_error
    def put(self, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().put(full_url, **kwargs)

    @raise_if_error
    def patch(self, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().patch(full_url, **kwargs)

    @raise_if_error
    def delete(self, url, **kwargs):
        full_url = urljoin(self.base_url, url)
        return super().delete(full_url, **kwargs)
