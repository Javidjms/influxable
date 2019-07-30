from . import settings
from .request import InfluxDBRequest


class Connection:
    def __init__(self):
        self.base_url = settings.INFLUXDB_URL
        self.user = settings.INFLUXDB_USER
        self.password = settings.INFLUXDB_PASSWORD
        self.database_name = settings.INFLUXDB_DATABASE_NAME

        self.request = InfluxDBRequest(self.base_url, self.database_name)
        self.request.auth = (self.user, self.password)
