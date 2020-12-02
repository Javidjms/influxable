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


class TestDBSelectQuery:
    def test_all_fields_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default"'
        res = query.execute()
        assert 'results' in res

    def test_one_field_success(self):
        query = Query()\
            .select('field1')\
            .from_measurements('default')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT field1 FROM "default"'
        res = query.execute()
        assert 'results' in res

    def test_two_field_success(self):
        query = Query()\
            .select('field1', 'field2')\
            .from_measurements('default')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT field1,field2 FROM "default"'
        res = query.execute()
        assert 'results' in res

    def test_with_function_success(self):
        query = Query()\
            .select(Abs('field1'))\
            .from_measurements('default')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT ABS(field1) FROM "default"'
        res = query.execute()
        assert 'results' in res

    def test_chain_success(self):
        query = Query()\
            .select('field1')\
            .select('field2')\
            .from_measurements('default')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT field2 FROM "default"'
        res = query.execute()
        assert 'results' in res

    def test_none_field_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select(None)\
                .from_measurements('default')


class TestDBIntoQuery:
    def test_one_measurement_success(self):
        query = Query()\
            .select()\
            .from_measurements('cpu')\
            .into('cpu_copy')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * INTO cpu_copy FROM "cpu"'
        res = query.execute()
        assert 'results' in res

    def test_chain_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .into('cpu_copy')\
            .into('cpu_copy_2')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * INTO cpu_copy_2 FROM "default"'
        res = query.execute()
        assert 'results' in res

    def test_with_bad_measurement_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('cpu')\
                .into(True)


class TestDBFromQuery:
    def test_one_measurement_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default"'
        res = query.execute()
        assert 'results' in res

    def test_two_measurement_success(self):
        query = Query()\
            .select()\
            .from_measurements('default', 'default_2')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default","default_2"'
        res = query.execute()
        assert 'results' in res

    def test_chain_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .from_measurements('default2')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default2"'
        res = query.execute()
        assert 'results' in res

    def test_with_empty_measurement_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements()

    def test_with_bad_measurement_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements(True)


