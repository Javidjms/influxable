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


class TestDBWhereQuery:
    def test_one_criteria_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .where(
                Field('value') > 800,
            )
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" WHERE "value" > 800'
        res = query.execute()
        assert 'results' in res

    def test_two_criteria_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .where(
                Field('value') < 400,
                Field('value') > 800,
            )
        prepared_query = query._get_prepared_query()
        test_query = 'SELECT * FROM "default" WHERE "value" < 400 AND "value" > 800'
        assert prepared_query == test_query
        res = query.execute()
        assert 'results' in res

    def test_with_function_success(self):
        pytest.skip()
        query = Query()\
            .select()\
            .from_measurements('default')\
            .where(
                Field(Abs('value')) < 400,
            )
        prepared_query = query._get_prepared_query()
        test_query = 'SELECT * FROM "default" WHERE "value" < 400 AND "value" > 800'
        assert prepared_query == test_query
        res = query.execute()
        assert 'results' in res

    def test_chain_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .where(
                Field('value') < 400,
            )\
            .where(
                Field('value') < 500,
            )
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" WHERE "value" < 500'
        res = query.execute()
        assert 'results' in res

    def test_with_empty_criteria_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .where()

    def test_with_bad_criteria_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .where(True)


class TestDBLimitQuery:
    def test_with_good_value_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .limit(10)
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" LIMIT 10'
        res = query.execute()
        assert 'results' in res

    def test_chain_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .limit(10)\
            .limit(100)
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" LIMIT 100'
        res = query.execute()
        assert 'results' in res

    def test_with_empty_fail(self):
        with pytest.raises(TypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .limit()

    def test_with_negative_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .limit(-10)

    def test_with_bad_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .limit(True)

    def test_with_decimal_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .limit(10.5)


class TestDBSLimitQuery:
    def test_with_good_value_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .slimit(10)
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" SLIMIT 10'
        res = query.execute()
        assert 'results' in res

    def test_chain_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .slimit(10)\
            .slimit(100)
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" SLIMIT 100'
        res = query.execute()
        assert 'results' in res

    def test_with_empty_fail(self):
        with pytest.raises(TypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .slimit()

    def test_with_negative_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .slimit(-10)

    def test_with_bad_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .slimit(True)

    def test_with_decimal_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .slimit(10.5)


class TestDBOffsetQuery:
    def test_with_good_value_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .offset(10)
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" OFFSET 10'
        res = query.execute()
        assert 'results' in res

    def test_chain_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .offset(10)\
            .offset(100)
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" OFFSET 100'
        res = query.execute()
        assert 'results' in res

    def test_with_empty_fail(self):
        with pytest.raises(TypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .offset()

    def test_with_negative_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .offset(-10)

    def test_with_bad_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .offset(True)

    def test_with_decimal_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .offset(10.5)


class TestDBSOffsetQuery:
    def test_with_good_value_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .soffset(10)
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" SOFFSET 10'
        res = query.execute()
        assert 'results' in res

    def test_chain_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .soffset(10)\
            .soffset(100)
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" SOFFSET 100'
        res = query.execute()
        assert 'results' in res

    def test_with_empty_fail(self):
        with pytest.raises(TypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .soffset()

    def test_with_negative_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .soffset(-10)

    def test_with_bad_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .soffset(True)

    def test_with_decimal_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .soffset(10.5)


