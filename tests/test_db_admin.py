import pytest
from influxable import Influxable, exceptions
from influxable.db import admin, InfluxDBAdmin, Field
from influxable.response import InfluxDBResponse


class TestGenericDBAdminCommand:
    def test_add_database_name_to_options_success(self):
        options = admin.GenericDBAdminCommand._add_database_name_to_options({})
        assert 'database_name' in options

    def test_execute_query_success(self):
        query = 'SHOW DATABASES'
        influx_response = admin.GenericDBAdminCommand._execute_query(query)
        assert isinstance(influx_response, InfluxDBResponse)
        assert influx_response.raw is not None
        assert influx_response.error is None

    def test_execute_query_failed(self):
        with pytest.raises(exceptions.InfluxDBError):
            query = 'SHOW MEASUREMENTS WHERE time < 200'
            admin.GenericDBAdminCommand._execute_query(query)

    def test_execute_query_with_parser_success(self):
        query = 'SHOW DATABASES'
        res = admin.GenericDBAdminCommand._execute_query_with_parser(query)
        assert isinstance(res, list)

    def test_get_formatted_privilege_success(self):
        privilege = admin.GenericDBAdminCommand._get_formatted_privilege('all')
        assert privilege == 'ALL'

    def test_get_formatted_privilege_success_2(self):
        privilege = admin.GenericDBAdminCommand._get_formatted_privilege(
            admin.Privileges.ALL
        )
        assert privilege == 'ALL'

    def test_get_formatted_privilege_failed(self):
        with pytest.raises(exceptions.InfluxDBInvalidChoiceError):
            admin.GenericDBAdminCommand._get_formatted_privilege('none')

    def test_get_formatted_user_name_success(self):
        name = admin.GenericDBAdminCommand._get_formatted_user_name('javid')
        assert name == '"javid"'

    def test_generate_from_clause_success(self):
        clause = admin.GenericDBAdminCommand._generate_from_clause(['param1'])
        assert clause == 'FROM "param1"'

    def test_generate_from_clause_with_two_measurement_success(self):
        clause = admin.GenericDBAdminCommand._generate_from_clause(
            ['param1', 'param2']
        )
        assert clause == 'FROM "param1", "param2"'

    def test_generate_from_clause_without_measurement_success(self):
        clause = admin.GenericDBAdminCommand._generate_from_clause([])
        assert clause == ''

    def test_generate_from_clause_failed(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            admin.GenericDBAdminCommand._generate_from_clause(True)

    def test_generate_where_clause_success(self):
        clause = admin.GenericDBAdminCommand._generate_where_clause(
            [Field('time') < 20]
        )
        assert clause == 'WHERE "time" < 20'



class TestShowAdminCommand:
    def test_show_field_key_cardinality_success(self):
        res = InfluxDBAdmin.show_field_key_cardinality()
        assert res is not None

    def test_show_field_key_cardinality_with_exact_success(self):
        res = InfluxDBAdmin.show_field_key_cardinality(exact=True)
        assert res is not None

    def test_show_measurement_cardinality_success(self):
        res = InfluxDBAdmin.show_measurement_cardinality()
        assert res is not None

    def test_show_measurement_cardinality_with_exact_success(self):
        res = InfluxDBAdmin.show_measurement_cardinality(exact=True)
        assert res is not None

    def test_show_series_cardinality_success(self):
        res = InfluxDBAdmin.show_series_cardinality()
        assert res is not None

    def test_show_series_cardinality_with_exact_success(self):
        res = InfluxDBAdmin.show_series_cardinality(exact=True)
        assert res is not None

    def test_show_tag_key_cardinality_success(self):
        res = InfluxDBAdmin.show_tag_key_cardinality()
        assert res is not None

    def test_show_tag_key_cardinality_with_exact_success(self):
        res = InfluxDBAdmin.show_tag_key_cardinality(exact=True)
        assert res is not None

    def test_show_tag_values_cardinality_success(self):
        res = InfluxDBAdmin.show_tag_values_cardinality('phase')
        assert res is not None

    def test_show_tag_values_cardinality_with_exact_success(self):
        res = InfluxDBAdmin.show_tag_values_cardinality('phase', exact=True)
        assert res is not None

    def test_show_continuous_queries_success(self):
        res = InfluxDBAdmin.show_continuous_queries()
        assert res is not None

    def test_show_diagnostics_success(self):
        res = InfluxDBAdmin.show_diagnostics()
        assert res is not None

    def test_show_field_keys_success(self):
        res = InfluxDBAdmin.show_field_keys()
        assert res is not None

    def test_show_field_keys_with_measurement_success(self):
        res = InfluxDBAdmin.show_field_keys(
            measurements=['param1'],
        )
        assert res is not None

    def test_show_field_keys_with_multiple_measurement_success(self):
        res = InfluxDBAdmin.show_field_keys(
            measurements=['param1', 'param2'],
        )
        assert res is not None

    def test_show_grants_success(self):
        res = InfluxDBAdmin.show_grants('admin')
        assert res is not None

    def test_show_databases_success(self):
        res = InfluxDBAdmin.show_databases()
        assert res is not None

    def test_show_measurements_success(self):
        res = InfluxDBAdmin.show_measurements()
        assert res is not None

    def test_show_measurements_with_criteria_success(self):
        res = InfluxDBAdmin.show_measurements(
            criteria=[Field('phase') == 'moon'],
        )
        assert res is not None

    def test_show_measurements_with_criteria_success_2(self):
        res = InfluxDBAdmin.show_measurements(
            criteria=[
                Field('phase') == 'moon',
                Field('phase') == 'sun',
            ],
        )
        assert res is not None

    def test_show_queries_success(self):
        res = InfluxDBAdmin.show_queries()
        assert res is not None

    def test_show_retention_policies_success(self):
        res = InfluxDBAdmin.show_retention_policies()
        assert res is not None

    def test_show_series_success(self):
        res = InfluxDBAdmin.show_series()
        assert res is not None

    def test_show_series_with_measurements_success(self):
        res = InfluxDBAdmin.show_series(
            measurements=['param1', 'param2'],
        )
        assert res is not None

    def test_show_series_with_criteria_success(self):
        res = InfluxDBAdmin.show_series(
            criteria=[Field('phase') == 'moon'],
        )
        assert res is not None

    def test_show_series_with_limit_success(self):
        res = InfluxDBAdmin.show_series(
            limit=10,
        )
        assert res is not None

    def test_show_series_with_offset_success(self):
        res = InfluxDBAdmin.show_series(
            offset=10,
        )
        assert res is not None

    def test_show_series_with_args_success(self):
        res = InfluxDBAdmin.show_series(
            measurements=['param1', 'param2'],
            criteria=[Field('phase') == 'moon'],
            limit=10,
            offset=10,
        )
        assert res is not None

    def test_show_stats_success(self):
        res = InfluxDBAdmin.show_stats()
        assert res is not None

    def test_show_shards_success(self):
        res = InfluxDBAdmin.show_shards()
        assert res is not None

    def test_show_shard_groups_success(self):
        res = InfluxDBAdmin.show_shard_groups()
        assert res is not None

    def test_show_subscriptions_success(self):
        res = InfluxDBAdmin.show_subscriptions()
        assert res is not None

    def test_show_tag_keys_success(self):
        res = InfluxDBAdmin.show_tag_keys()
        assert res is not None

    def test_show_tag_keys_with_measurement_success(self):
        res = InfluxDBAdmin.show_tag_keys(measurements=['param1'])
        assert res is not None

    def test_show_tag_keys_with_measurements_success(self):
        res = InfluxDBAdmin.show_tag_keys(measurements=['param1', 'param2'])
        assert res is not None

    def test_show_tag_values_success(self):
        res = InfluxDBAdmin.show_tag_values('phase')
        assert res is not None

    def test_show_tag_values_with_measurement_success(self):
        res = InfluxDBAdmin.show_tag_values(
            'phase',
            measurements=['param1'],
        )
        assert res is not None

    def test_show_tag_values_with_measurements_success(self):
        res = InfluxDBAdmin.show_tag_values(
            'phase',
            measurements=['param1', 'param2'],
        )
        assert res is not None

    def test_show_users_success(self):
        res = InfluxDBAdmin.show_users()
        assert res is not None
