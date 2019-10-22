from .. import Influxable, exceptions, serializers
from .criteria import Criteria
from .query import RawQuery
from ..response import InfluxDBResponse


class Privileges:
    ALL = 'ALL'
    READ = 'READ'
    WRITE = 'WRITE'


PRIVILEGE_VALUES = ['ALL', 'READ', 'WRITE']


class GenericDBAdminCommand:
    @staticmethod
    def _add_database_name_to_options(options):
        database_name = GenericDBAdminCommand._get_database_name()
        database_name = GenericDBAdminCommand._format_with_double_quote(
            database_name
        )
        options.update({'database_name': database_name})
        return options

    @staticmethod
    def _execute_query(query, options={}):
        options = GenericDBAdminCommand._add_database_name_to_options(options)
        prepared_query = query.format(**options)
        response = RawQuery(prepared_query).execute()
        influx_response = InfluxDBResponse(response)
        influx_response.raise_if_error()
        return influx_response

    @staticmethod
    def _execute_query_with_parser(
        query,
        parser=serializers.FlatFormattedSerieSerializer,
        options={},
    ):
        influx_response = GenericDBAdminCommand._execute_query(query, options)
        formatted_result = parser(influx_response).convert()
        return formatted_result

    @staticmethod
    def _get_formatted_privilege(privilege):
        privilege = str(privilege).upper()
        if privilege not in PRIVILEGE_VALUES:
            msg = 'privilege `{}` must be one of value of {}'.format(
                privilege,
                PRIVILEGE_VALUES,
            )
            raise exceptions.InfluxDBInvalidChoiceError(msg)
        return privilege

    @staticmethod
    def _get_formatted_user_name(user_name):
        return GenericDBAdminCommand._format_with_double_quote(user_name)

    @staticmethod
    def _generate_from_clause(measurements):
        if not isinstance(measurements, list):
            msg = 'measurements type must be <list>'
            raise exceptions.InfluxDBInvalidTypeError(msg)

        quoted_measurements = ['"{}"'.format(m) for m in measurements]
        selected_measurements = ', '.join(quoted_measurements)

        from_clause = ''
        if selected_measurements:
            from_clause = 'FROM {}'.format(selected_measurements)
        return from_clause

    @staticmethod
    def _generate_where_clause(criteria):
        if not isinstance(criteria, list):
            msg = 'criteria type must be <list>'
            raise exceptions.InfluxDBInvalidTypeError(msg)

        if len(criteria) and \
           not any([isinstance(c, Criteria) for c in criteria]):
            msg = 'criteria type must be <list> of <Criteria>'
            raise exceptions.InfluxDBInvalidTypeError(msg)

        where_clause = ''
        if len(criteria):
            selected_criteria = [c.evaluate() for c in criteria]
            eval_criteria = ' AND '.join(selected_criteria)
            where_clause = 'WHERE {}'.format(eval_criteria)
        return where_clause

    @staticmethod
    def _generate_limit_clause(limit):
        if limit is not None and not isinstance(limit, int):
            msg = 'limit type must be <int>'
            raise exceptions.InfluxDBInvalidTypeError(msg)

        limit_clause = ''
        if limit is not None:
            limit_clause = 'LIMIT {}'.format(limit)
        return limit_clause

    @staticmethod
    def _generate_offset_clause(offset):
        if offset is not None and not isinstance(offset, int):
            msg = 'offset type must be <int>'
            raise exceptions.InfluxDBInvalidTypeError(msg)

        offset_clause = ''
        if offset is not None:
            offset_clause = 'OFFSET {}'.format(offset)
        return offset_clause

    @staticmethod
    def _generate_default_clause(is_default):
        return 'DEFAULT' if is_default is True else ''

    @staticmethod
    def _generate_duration_clause(duration):
        return 'DURATION {}'.format(duration) if duration else ''

    @staticmethod
    def _generate_replication_clause(replication):
        return 'REPLICATION {}'.format(replication) if replication else ''

    @staticmethod
    def _generate_shard_duration_clause(sh_duration):
        return 'SHARD DURATION {}'.format(sh_duration) if sh_duration else ''

    @staticmethod
    def _get_database_name():
        instance = GenericDBAdminCommand._get_influxable_instance()
        database_name = instance.database_name
        return database_name

    @staticmethod
    def _get_influxable_instance():
        instance = Influxable.get_instance()
        return instance

    @staticmethod
    def _format_with_simple_quote(string):
        return '\'{}\''.format(string)

    @staticmethod
    def _format_with_double_quote(string):
        return '"{}"'.format(string)


class AlterAdminCommand:
    @staticmethod
    def alter_retention_policy(
        policy_name,
        duration=None,
        replication=None,
        shard_duration=None,
        is_default=False,
    ):
        policy_name = GenericDBAdminCommand._format_with_double_quote(
            policy_name,
        )

        default_clause = GenericDBAdminCommand._generate_default_clause(
            is_default
        )
        duration_clause = GenericDBAdminCommand._generate_duration_clause(
            duration
        )
        replication_clause = GenericDBAdminCommand._generate_replication_clause(
            replication
        )
        shard_duration_clause = GenericDBAdminCommand._generate_shard_duration_clause(
            shard_duration
        )

        options = {
            'default_clause': default_clause,
            'duration_clause': duration_clause,
            'policy_name': policy_name,
            'replication_clause': replication_clause,
            'shard_duration_clause': shard_duration_clause,
        }
        query = 'ALTER RETENTION POLICY {policy_name} ON {database_name}' +\
                ' {duration_clause}' +\
                ' {replication_clause}' +\
                ' {shard_duration_clause}' +\
                ' {default_clause}'
        InfluxDBAdmin._execute_query(query, options)
        return True


class CreateAdminCommand:
    @staticmethod
    def create_continuous_query():
        raise NotImplementedError

    @staticmethod
    def create_database(
        database_name,
        duration=None,
        replication=None,
        shard_duration=None,
        policy_name=None,
    ):
        database_name = GenericDBAdminCommand._format_with_double_quote(
            database_name,
        )
        options = {'database_name': database_name}

        with_clause = ''
        if duration or replication or shard_duration or policy_name:
            policy_clause = ''
            if policy_name:
                policy_clause = 'NAME "{}"'.format(policy_name)

            duration_clause = GenericDBAdminCommand._generate_duration_clause(
                duration
            )
            replication_clause = GenericDBAdminCommand._generate_replication_clause(
                replication
            )
            shard_duration_clause = GenericDBAdminCommand._generate_shard_duration_clause(
                shard_duration
            )

            with_clause = 'WITH' +\
                          ' {duration_clause}' +\
                          ' {replication_clause}' +\
                          ' {shard_duration_clause}' +\
                          ' {policy_clause}'
            options.update({
                'duration_clause': duration_clause,
                'replication_clause': replication_clause,
                'policy_clause': policy_clause,
                'shard_duration_clause': shard_duration_clause,
            })
        query = 'CREATE DATABASE {database_name}' + with_clause
        InfluxDBAdmin._execute_query(query, options)
        return True

    @staticmethod
    def create_retention_policy(
        policy_name,
        duration=None,
        replication=None,
        shard_duration=None,
        is_default=False,
    ):
        policy_name = GenericDBAdminCommand._format_with_double_quote(
            policy_name,
        )

        default_clause = GenericDBAdminCommand._generate_default_clause(
            is_default
        )
        duration_clause = GenericDBAdminCommand._generate_duration_clause(
            duration
        )
        replication_clause = GenericDBAdminCommand._generate_replication_clause(
            replication
        )
        shard_duration_clause = GenericDBAdminCommand._generate_shard_duration_clause(
            shard_duration
        )

        options = {
            'default_clause': default_clause,
            'duration_clause': duration_clause,
            'replication_clause': replication_clause,
            'policy_name': policy_name,
            'shard_duration_clause': shard_duration_clause,
        }
        query = 'CREATE RETENTION POLICY {policy_name} ON {database_name}' +\
                ' {duration_clause}' +\
                ' {replication_clause}' +\
                ' {shard_duration_clause}' +\
                ' {default_clause}'
        InfluxDBAdmin._execute_query(query, options)
        return True

    @staticmethod
    def create_subscription(subscription_name, hosts, any=False):
        subscription_name = GenericDBAdminCommand._format_with_double_quote(
            subscription_name,
        )
        destination_type = 'ANY' if any else 'ALL'
        formatted_hosts = ', '.join(['\'{}\''.format(h) for h in hosts])
        options = {
            'hosts': formatted_hosts,
            'destination_type': destination_type,
            'subscription_name': subscription_name,
        }
        query = 'CREATE SUBSCRIPTION {subscription_name} ON {database_name}' +\
                ' DESTINATIONS {destination_type} {hosts}'
        InfluxDBAdmin._execute_query(query, options)
        return True

    @staticmethod
    def create_user(user_name, password, with_privileges=False):
        user_name = GenericDBAdminCommand._get_formatted_user_name(user_name)
        password = GenericDBAdminCommand._format_with_simple_quote(
            password,
        )
        privilege_clause = 'WITH ALL PRIVILEGES' if with_privileges else ''
        options = {
            'user_name': user_name,
            'password': password,
            'privilege_clause': privilege_clause,
        }
        query = 'CREATE USER {user_name} WITH PASSWORD {password}' +\
                ' {privilege_clause}'
        InfluxDBAdmin._execute_query(query, options)
        return True


class DeleteAdminCommand:
    @staticmethod
    def delete(measurements, criteria):
        from_clause = GenericDBAdminCommand._generate_from_clause(measurements)
        where_clause = GenericDBAdminCommand._generate_where_clause(criteria)

        if not from_clause and not where_clause:
            msg = '`measurements` or `criteria` must be not null'
            raise exceptions.InfluxDBError(msg)

        options = {
            'from_clause': from_clause,
            'where_clause': where_clause,
        }
        query = 'DELETE {from_clause} {where_clause}'
        InfluxDBAdmin._execute_query(query, options)
        return True


        query = 'SHOW FIELD KEY {exact} CARDINALITY'
        query = query.format(**options)
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_measurement_cardinality(exact=False):
        options = {
            'exact': 'EXACT' if exact else '',
        }
        query = 'SHOW MEASUREMENT {exact} CARDINALITY'
        query = query.format(**options)
        parser = serializers.FlatSingleValueSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_series_cardinality(exact=False):
        options = {
            'exact': 'EXACT' if exact else '',
        }
        query = 'SHOW SERIES {exact} CARDINALITY'
        query = query.format(**options)
        parser = serializers.FlatSingleValueSerializer
        if exact:
            parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_tag_key_cardinality(exact=False):
        options = {
            'exact': 'EXACT' if exact else '',
        }
        query = 'SHOW TAG KEY {exact} CARDINALITY'
        query = query.format(**options)
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_tag_values_cardinality(key, exact=False):
        options = {
            'key': key,
            'exact': 'EXACT' if exact else '',
        }
        query = 'SHOW TAG VALUES {exact} CARDINALITY WITH KEY = "{key}"'
        query = query.format(**options)
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_continuous_queries():
        query = 'SHOW CONTINUOUS QUERIES'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_diagnostics():
        query = 'SHOW DIAGNOSTICS'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_field_keys(*measurements):
        quoted_measurements = ['"{}"'.format(m) for m in measurements]
        selected_measurements = ', '.join(quoted_measurements)
        if selected_measurements:
            from_clause = 'FROM {}'.format(selected_measurements)
        else:
            from_clause = ''
        options = {'from_clause': from_clause}
        query = 'SHOW FIELD KEYS {from_clause}'
        query = query.format(**options)
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_grants(username):
        options = {'username': username}
        query = 'SHOW GRANTS FOR {username}'
        query = query.format(**options)
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_databases():
        query = 'SHOW DATABASES'
        parser = serializers.FlatSimpleResultSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_measurements(*criteria):
        query = 'SHOW MEASUREMENTS {where_clause}'
        selected_criteria = [c.evaluate() for c in criteria]
        eval_criteria = ' AND '.join(selected_criteria)
        if eval_criteria:
            where_clause = 'WHERE {}'.format(eval_criteria)
        else:
            where_clause = ''
        options = {'where_clause': where_clause}
        query = query.format(**options)
        parser = serializers.FlatSimpleResultSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_queries():
        query = 'SHOW QUERIES'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_retention_policies():
        query = 'SHOW RETENTION POLICIES'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_series():
        query = 'SHOW SERIES'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_stats():
        query = 'SHOW STATS'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_shards():
        query = 'SHOW SHARDS'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_shard_groups():
        query = 'SHOW SHARD GROUPS'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_subscriptions():
        query = 'SHOW SUBSCRIPTIONS'
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_tag_keys(*measurements):
        quoted_measurements = ['"{}"'.format(m) for m in measurements]
        selected_measurements = ', '.join(quoted_measurements)
        if selected_measurements:
            from_clause = 'FROM {}'.format(selected_measurements)
        else:
            from_clause = ''
        options = {'from_clause': from_clause}
        query = 'SHOW TAG KEYS {from_clause}'
        query = query.format(**options)
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_tag_values(key, *measurements):
        quoted_measurements = ['"{}"'.format(m) for m in measurements]
        selected_measurements = ', '.join(quoted_measurements)
        if selected_measurements:
            from_clause = 'FROM {}'.format(selected_measurements)
        else:
            from_clause = ''
        options = {
            'key': key,
            'from_clause': from_clause,
        }
        query = 'SHOW TAG VALUES {from_clause} WITH KEY = "{key}"'
        query = query.format(**options)
        parser = serializers.FormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_users():
        query = 'SHOW USERS'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)


class InfluxDBAdmin(
    ShowAdminCommand,
):
    pass
