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

        options = {
            'exact': 'EXACT' if exact else '',
        }
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
