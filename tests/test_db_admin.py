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

    def test_generate_where_clause_with_two_measurement_success(self):
        clause = admin.GenericDBAdminCommand._generate_where_clause(
            [
                Field('time') < 20,
                Field('phase') == 'MOON',
            ]
        )
        assert clause == 'WHERE "time" < 20 AND "phase" = \'MOON\''

    def test_generate_where_clause_without_measurement_success(self):
        clause = admin.GenericDBAdminCommand._generate_where_clause([])
        assert clause == ''

    def test_generate_where_clause_failed(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            admin.GenericDBAdminCommand._generate_where_clause(True)

    def test_generate_limit_clause_success(self):
        clause = admin.GenericDBAdminCommand._generate_limit_clause(10)
        assert clause == 'LIMIT 10'

    def test_generate_limit_clause_failed(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            admin.GenericDBAdminCommand._generate_limit_clause("test")

    def test_generate_offset_clause_success(self):
        clause = admin.GenericDBAdminCommand._generate_offset_clause(10)
        assert clause == 'OFFSET 10'

    def test_generate_offset_clause_failed(self):
        with pytest.raises(exceptions.InfluxDBInvalidTypeError):
            admin.GenericDBAdminCommand._generate_offset_clause("test")

    def test_generate_default_clause_success_1(self):
        clause = admin.GenericDBAdminCommand._generate_default_clause(True)
        assert clause == 'DEFAULT'

    def test_generate_default_clause_success_2(self):
        clause = admin.GenericDBAdminCommand._generate_default_clause(False)
        assert clause == ''

    def test_generate_duration_clause_success_1(self):
        clause = admin.GenericDBAdminCommand._generate_duration_clause('1d')
        assert clause == 'DURATION 1d'

    def test_generate_duration_clause_success_2(self):
        clause = admin.GenericDBAdminCommand._generate_duration_clause()
        assert clause == ''

    def test_generate_replication_clause_success_1(self):
        clause = admin.GenericDBAdminCommand._generate_replication_clause(4)
        assert clause == 'REPLICATION 4'

    def test_generate_replication_clause_success_2(self):
        clause = admin.GenericDBAdminCommand._generate_replication_clause()
        assert clause == ''

    def test_generate_shard_duration_clause_success_1(self):
        clause = admin.GenericDBAdminCommand._generate_shard_duration_clause('4d')
        assert clause == 'SHARD DURATION 4d'

    def test_generate_shard_duration_clause_success_2(self):
        clause = admin.GenericDBAdminCommand._generate_shard_duration_clause()
        assert clause == ''

    def test_get_influxable_instance_success(self):
        instance = admin.GenericDBAdminCommand._get_influxable_instance()
        assert isinstance(instance, Influxable)

    def test_format_with_simple_quote_success(self):
        string = admin.GenericDBAdminCommand._format_with_simple_quote('test')
        assert string == '\'test\''

    def test_format_with_double_quote_success(self):
        string = admin.GenericDBAdminCommand._format_with_double_quote('test')
        assert string == '"test"'


class TestAlterAdminCommand:
    @classmethod
    def setup_class(cls):
        InfluxDBAdmin.create_retention_policy(
            'test_policy',
            duration='1d',
            replication=3,
        )

    def test_alter_retention_policy_success_1(self):
        res = InfluxDBAdmin.alter_retention_policy(
            'test_policy',
            duration='1d',
        )
        assert res is True

    def test_alter_retention_policy_success_2(self):
        res = InfluxDBAdmin.alter_retention_policy(
            'test_policy',
            replication=4,
        )
        assert res is True

    def test_alter_retention_policy_success_3(self):
        res = InfluxDBAdmin.alter_retention_policy(
            'test_policy',
            shard_duration='1h',
        )
        assert res is True

    def test_alter_retention_policy_failed(self):
        with pytest.raises(exceptions.InfluxDBError):
            InfluxDBAdmin.alter_retention_policy(
                'test_policy'
            )


class TestCreateAdminCommand:
    def test_create_database_success_1(self):
        res = InfluxDBAdmin.create_database(
            'test_database_1',
        )
        assert res is True

    def test_create_database_success_2(self):
        res = InfluxDBAdmin.create_database(
            'test_database_2',
            duration='1d',
        )
        assert res is True

    def test_create_database_success_3(self):
        res = InfluxDBAdmin.create_database(
            'test_database_3',
            replication=4,
        )
        assert res is True

    def test_create_database_success_4(self):
        res = InfluxDBAdmin.create_database(
            'test_database_4',
            shard_duration='1h',
        )
        assert res is True

    def test_create_database_success_5(self):
        res = InfluxDBAdmin.create_database(
            'test_database_5',
            policy_name='test_policy_2',
        )
        assert res is True

    def test_create_retention_policy_success_1(self):
        res = InfluxDBAdmin.create_retention_policy(
            'test_policy_1',
            duration='1d',
            replication=3,
        )
        assert res is True

    def test_create_retention_policy_success_2(self):
        res = InfluxDBAdmin.create_retention_policy(
            'test_policy_22',
            duration='1d',
            replication=4,
        )
        assert res is True

    def test_create_retention_policy_success_3(self):
        res = InfluxDBAdmin.create_retention_policy(
            'test_policy_3',
            duration='1d',
            replication=4,
            shard_duration='1h',
        )
        assert res is True

    def test_create_retention_policy_failed_1(self):
        with pytest.raises(exceptions.InfluxDBError):
            InfluxDBAdmin.create_retention_policy(
                'test_policy'
            )

    def test_create_retention_policy_failed_2(self):
        with pytest.raises(exceptions.InfluxDBError):
            InfluxDBAdmin.create_retention_policy(
                'test_policy',
                replication=4,
                shard_duration='1h',
            )

    def test_create_retention_policy_failed_3(self):
        with pytest.raises(exceptions.InfluxDBError):
            InfluxDBAdmin.create_retention_policy(
                'test_policy',
                duration='1d',
                shard_duration='1h',
            )

    def test_create_retention_policy_failed_4(self):
        with pytest.raises(exceptions.InfluxDBError):
            InfluxDBAdmin.create_retention_policy(
                'test_policy',
                replication=4,
            )

    def test_create_subscription_success_1(self):
        res = InfluxDBAdmin.create_subscription(
            'test_subscription_1',
            hosts=["http://localhost:5000"],
        )
        assert res is True
        InfluxDBAdmin.drop_subscription('test_subscription_1')

    def test_create_subscription_success_2(self):
        res = InfluxDBAdmin.create_subscription(
            'test_subscription_2',
            hosts=["http://localhost:5000", "http://localhost:6000"],
            any=True,
        )
        assert res is True
        InfluxDBAdmin.drop_subscription('test_subscription_2')

    def test_create_user_success_1(self):
        res = InfluxDBAdmin.create_user(
            user_name='user_test_1',
            password='password_test_1',
        )
        assert res is True

    def test_create_user_success_2(self):
        res = InfluxDBAdmin.create_user(
            user_name='user_test_2',
            password='password_test_2',
            with_privileges=True,
        )
        assert res is True


class TestDeleteAdminCommand:
    def test_delete_success_1(self):
        res = InfluxDBAdmin.delete(
            measurements=['mymeas'],
        )
        assert res is True

    def test_delete_success_2(self):
        res = InfluxDBAdmin.delete(
            criteria=[Field('time') < 10],
        )
        assert res is True

    def test_delete_failed(self):
        with pytest.raises(exceptions.InfluxDBError):
            InfluxDBAdmin.delete()


class TestDropAdminCommand:
    def test_drop_continuous_query_success(self):
        res = InfluxDBAdmin.drop_continuous_query('test_continuous_query')
        assert res is True

    def test_drop_database_success(self):
        res = InfluxDBAdmin.drop_database('test_database')
        assert res is True

    def test_drop_measurement_success(self):
        res = InfluxDBAdmin.drop_measurement('test_measurement')
        assert res is True

    def test_drop_retention_policy_success(self):
        res = InfluxDBAdmin.drop_retention_policy('test_policy')
        assert res is True

    def test_drop_series_success_1(self):
        res = InfluxDBAdmin.drop_series(measurements=['mymeas'])
        assert res is True

    def test_drop_series_success_2(self):
        res = InfluxDBAdmin.drop_series(criteria=[Field('phase') == 'moon'])
        assert res is True

    def test_drop_series_failed(self):
        with pytest.raises(exceptions.InfluxDBError):
            InfluxDBAdmin.drop_series()

    def test_drop_shard_success(self):
        res = InfluxDBAdmin.drop_shard(1)
        assert res is True

    def test_drop_subscription_success(self):
        pytest.skip("SKIP")
        res = InfluxDBAdmin.drop_subscription('test_subscription')
        assert res is True

    def test_drop_user_success(self):
        pytest.skip("SKIP")
        res = InfluxDBAdmin.drop_user('test_user')
        assert res is True


class TestExplainAdminCommand:
    def test_explain_success_1(self):
        query = 'SELECT * FROM mymeas LIMIT 10'
        res = InfluxDBAdmin.explain(query)
        assert res is not None

    def test_explain_success_2(self):
        query = 'SELECT * FROM mymeas LIMIT 10'
        res = InfluxDBAdmin.explain(query, analyze=True)
        assert res is not None


class TestGrantAdminCommand:
    def test_grant_success(self):
        res = InfluxDBAdmin.grant(admin.Privileges.ALL, 'user_test_1')
        assert res is not None


class TestRevokeAdminCommand:
    def test_revoke_success(self):
        res = InfluxDBAdmin.revoke(admin.Privileges.ALL, 'user_test_1')
        assert res is not None


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
