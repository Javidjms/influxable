import pytest
from influxable.db.criteria import Field
from influxable.db.query import RawQuery, Query, BulkInsertQuery
from influxable.db.function.transformations import Abs
from influxable import exceptions


class TestDBRawQuery:
    def test_execute_query_success(self):
        str_query = 'SHOW DATABASES'
        raw_query = RawQuery(str_query)
        assert raw_query.query == str_query
        res = raw_query.execute()
        assert 'results' in res

    def test_execute_query_empty_query_fail(self):
        with pytest.raises(exceptions.InfluxDBEmptyRequestError):
            str_query = ''
            raw_query = RawQuery(str_query)
            raw_query.execute()

    def test_execute_query_bad_query_fail(self):
        with pytest.raises(exceptions.InfluxDBBadQueryError):
            str_query = 'SELECT *'
            raw_query = RawQuery(str_query)
            raw_query.execute()


