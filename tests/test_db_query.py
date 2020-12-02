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


class TestGroupByTagQuery:
    def test_with_all_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .group_by()
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" GROUP BY *'
        res = query.execute()
        assert 'results' in res

    def test_with_one_tag_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .group_by('tag_1')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" GROUP BY tag_1'
        res = query.execute()
        assert 'results' in res

    def test_with_two_tag_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .group_by('tag_1', 'tag_2')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" GROUP BY tag_1, tag_2'
        res = query.execute()
        assert 'results' in res

    def test_chain_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .group_by('tag_1', 'tag_2')\
            .group_by('tag_3')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" GROUP BY tag_3'
        res = query.execute()
        assert 'results' in res

    def test_with_bad_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .group_by(True)


class TestGroupByTimeQuery:
    def test_with_good_interval_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .range_by('12s')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" GROUP BY time(12s)'
        res = query.execute()
        assert 'results' in res

    def test_with_good_shift_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .range_by('12s', shift='1d')
        prepared_query = query._get_prepared_query()
        expected_query = 'SELECT * FROM "default" GROUP BY time(12s,1d)'
        assert prepared_query == expected_query
        res = query.execute()
        assert 'results' in res

    def test_with_negative_shift_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .range_by('12s', shift='-1d')
        prepared_query = query._get_prepared_query()
        expected_query = 'SELECT * FROM "default" GROUP BY time(12s,-1d)'
        assert prepared_query == expected_query
        res = query.execute()
        assert 'results' in res

    def test_with_one_tag_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .range_by('12s', tags=['tag1'])
        prepared_query = query._get_prepared_query()
        expected_query = 'SELECT * FROM "default" GROUP BY time(12s),tag1'
        assert prepared_query == expected_query
        res = query.execute()
        assert 'results' in res

    def test_with_two_tags_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .range_by('12s', tags=['tag1', 'tag2'])
        prepared_query = query._get_prepared_query()
        expected_query = 'SELECT * FROM "default" GROUP BY time(12s),tag1,tag2'
        assert prepared_query == expected_query
        res = query.execute()
        assert 'results' in res

    def test_with_fill_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .range_by('12s', fill=3)
        prepared_query = query._get_prepared_query()
        expected_query = 'SELECT * FROM "default" GROUP BY time(12s) fill(3)'
        assert prepared_query == expected_query
        res = query.execute()
        assert 'results' in res

    def test_with_shift_and_fill_and_tags_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .range_by('12s', shift='1d', tags=['tag1'], fill=3)
        prepared_query = query._get_prepared_query()
        expected_query = 'SELECT * FROM "default" GROUP BY time(12s,1d),tag1 fill(3)'
        assert prepared_query == expected_query
        res = query.execute()
        assert 'results' in res

    def test_chain_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .range_by('12s')\
            .range_by('5s')
        prepared_query = query._get_prepared_query()
        expected_query = 'SELECT * FROM "default" GROUP BY time(5s)'
        assert prepared_query == expected_query
        res = query.execute()
        assert 'results' in res

    def test_with_fill_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .range_by('12s', fill=True)

    def test_with_bad_tags_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .range_by('12s', tags=True)

    def test_with_bad_tags_fail_2(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .range_by('12s', tags=[1, 2])

    def test_with_bad_interval(self):
        with pytest.raises(exceptions.InfluxDBBadQueryError):
            query = Query()\
                .select()\
                .from_measurements('default')\
                .range_by('12k')
            query.execute()

    def test_with_bad_shift(self):
        with pytest.raises(exceptions.InfluxDBBadQueryError):
            query = Query()\
                .select()\
                .from_measurements('default')\
                .range_by('12s', shift='12k')
            query.execute()



class TestOrderByQuery:
    def test_asc_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .asc()
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" ORDER BY ASC'
        res = query.execute()
        assert 'results' in res

    def test_desc_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .desc()
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" ORDER BY DESC'
        res = query.execute()
        assert 'results' in res

    def test_chain_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .desc()\
            .asc()\
            .desc()
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" ORDER BY DESC'
        res = query.execute()
        assert 'results' in res


class TestTimezoneQuery:
    def test_with_good_value_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .tz('Europe/Paris')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" tz(\'Europe/Paris\')'
        res = query.execute()
        assert 'results' in res

    def test_chain_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .tz('Europe/London')\
            .tz('Europe/Paris')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT * FROM "default" tz(\'Europe/Paris\')'
        res = query.execute()
        assert 'results' in res

    def test_with_bad_value_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .tz(True)

    def test_with_bad_timezone_fail(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            Query()\
                .select()\
                .from_measurements('default')\
                .tz('Paris')


class TestSelectAggregation:
    def test_count_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .count()
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT COUNT(*) FROM "default"'
        res = query.execute()
        assert 'results' in res

    def test_count_with_value_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .count('value')
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT COUNT(value) FROM "default"'
        res = query.execute()
        assert 'results' in res

    def test_distinct_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .distinct()
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT DISTINCT(*) FROM "default"'
        res = query.execute()
        assert 'results' in res

    def test_mean_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .mean()
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT MEAN(*) FROM "default"'
        res = query.execute()
        assert 'results' in res

    def test_sum_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .sum()
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT SUM(*) FROM "default"'
        res = query.execute()
        assert 'results' in res

    def test_median_success(self):
        query = Query()\
            .select()\
            .from_measurements('default')\
            .median()
        prepared_query = query._get_prepared_query()
        assert prepared_query == 'SELECT MEDIAN(*) FROM "default"'
        res = query.execute()
        assert 'results' in res
