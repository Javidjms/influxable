import pytest
import requests
from influxable import Influxable, InfluxDBApi, exceptions


class TestInfluxApi:
    def get_instance(self):
        instance = Influxable.get_instance()
        return instance

