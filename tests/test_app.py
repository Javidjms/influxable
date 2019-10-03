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

    def test_singleton_create_second_instance_error(self):
        with pytest.raises(TypeError):
            self.create_instance_of_influxable()

    def test_ping_success(self):
        instance = self.get_instance()
        res = instance.ping()
        assert res is True

    def test_execute_query_success(self):
        query = 'SHOW DATABASES'
        instance = self.get_instance()
        res = instance.execute_query(query=query)
        assert res != {}

    def test_write_points_success(self):
        instance = self.get_instance()
        points = 'mysensor,esn=12,phase=moon value=10 1463289075000000000'
        res = instance.write_points(points)
        assert res is True
