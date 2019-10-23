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

    def test_get_debug_vars_success(self):
        instance = self.get_instance()
        res = InfluxDBApi.get_debug_vars(instance.connection.request)
        assert res is not None

    def test_ping_success(self):
        instance = self.get_instance()
        res = InfluxDBApi.ping(instance.connection.request)
        assert res is True

    def test_ping_verbose_success(self):
        instance = self.get_instance()
        res = InfluxDBApi.ping(instance.connection.request, verbose=True)
        assert res is not None
        assert 'version' in res

    def test_ping_verbose_silent_fail(self):
        instance = self.get_instance()
        res = InfluxDBApi.ping(instance.connection.request, verbose='k')
        assert res is True

    def test_execute_query_success(self):
        query = 'SHOW DATABASES'
        instance = self.get_instance()
        res = InfluxDBApi.execute_query(instance.connection.request, query)
        assert res is not None
        assert 'results' in res

    def test_execute_query_bad_query_fail(self):
        with pytest.raises(exceptions.InfluxDBBadQueryError):
            query = 'SELECT *'
            instance = self.get_instance()
            InfluxDBApi.execute_query(instance.connection.request, query)

    def test_execute_query_bad_method_fail(self):
        with pytest.raises(requests.exceptions.HTTPError):
            query = 'SHOW DATABASES'
            instance = self.get_instance()
            InfluxDBApi.execute_query(
                instance.connection.request,
                query,
                method='delete',
            )

    def test_write_points_success(self):
        precision = 's'
        points = 'mymeas,mytag=1 myfield=90 1463683075'
        instance = self.get_instance()
        res = InfluxDBApi.write_points(
            instance.connection.request,
            points,
            precision,
        )
        assert res is True

    def test_write_points_without_ts_success(self):
        precision = 's'
        points = 'mymeas,mytag=2 myfield=91'
        instance = self.get_instance()
        res = InfluxDBApi.write_points(
            instance.connection.request,
            points,
            precision,
        )
        assert res is True

    def test_write_points_multiple_success(self):
        precision = 's'
        points = '''
        mymeas,mytag=1 myfield=90 1463683075
        mymeas,mytag=3 myfield=34 1463683025
        '''
        instance = self.get_instance()
        res = InfluxDBApi.write_points(
            instance.connection.request,
            points,
            precision,
        )
        assert res is True

    def test_write_points_with_policy_success(self):
        rp = 'myrp'
        points = 'mymeas,mytag=1 myfield=90'
        instance = self.get_instance()
        res = InfluxDBApi.write_points(
            instance.connection.request,
            points,
            retention_policy_name=rp,
        )
        assert res is True

    def test_write_points_bad_timestamp_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTimestampError):
            points = 'mymeas,mytag=1 myfield=90 invalid'
            instance = self.get_instance()
            InfluxDBApi.write_points(
                instance.connection.request,
                points,
            )
