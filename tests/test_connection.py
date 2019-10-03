import pytest
from influxable import InfluxDBApi, exceptions
from influxable.connection import Connection


class TestConnection:
    def check_if_connection_reached(self, connection):
        query = 'SHOW DATABASES'
        InfluxDBApi.execute_query(connection.request, query)

