from . import settings
from .request import InfluxDBRequest


class Connection:
    def __init__(self, *args, **kwargs):
        self.base_url = kwargs.get('base_url', settings.INFLUXDB_URL)
        self.user = kwargs.get('user', settings.INFLUXDB_USER)
        self.password = kwargs.get('password', settings.INFLUXDB_PASSWORD)
        self.database_name = kwargs.get(
            'database_name',
            settings.INFLUXDB_DATABASE_NAME,
        )

        self.request = InfluxDBRequest(self.base_url, self.database_name)
        self.request.auth = (self.user, self.password)

    @staticmethod
    def create(base_url, database_name, user='', password=''):
        return Connection(base_url, database_name, user, password)
