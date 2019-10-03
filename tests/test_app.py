import pytest
from influxable import Influxable


class TestApp:
    def create_instance_of_influxable(self):
        instance = Influxable()
        return instance

    def get_instance(self):
        instance = Influxable.get_instance()
        return instance

    def test_singleton_first_instance_success(self):
        first_instance = self.create_instance_of_influxable()
        second_instance = self.get_instance()
        assert first_instance == second_instance

    def test_singleton_get_instance_success(self):
        instance = self.get_instance()
        assert instance is not None

