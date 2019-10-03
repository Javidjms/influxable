import pytest
import requests
from influxable import Influxable, InfluxDBApi, exceptions


class TestInfluxApi:
    def get_instance(self):
        instance = Influxable.get_instance()
        return instance

    def test_get_debug_requests_success(self):
        instance = self.get_instance()
        res = InfluxDBApi.get_debug_requests(
            instance.connection.request,
            seconds=10,
        )
        assert res is not None

    def test_get_debug_requests_silent_fail(self):
        instance = self.get_instance()
        res = InfluxDBApi.get_debug_requests(
            instance.connection.request,
            seconds='k',
        )
        assert res is not None

