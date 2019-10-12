from .query import RawQuery
from ..response import InfluxDBResponse
from .. import serializers


class InfluxDBAdmin:
    @staticmethod
    def _execute_query(query, parser=serializers.FlatFormattedSerieSerializer):
        response = RawQuery(query).execute()
        influx_response = InfluxDBResponse(response)
        formatted_result = parser(influx_response).convert()
        return formatted_result

    @staticmethod
    def show_field_key_cardinality(exact=False):
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
    def show_measurements():
        query = 'SHOW MEASUREMENTS'
        parser = serializers.FlatSimpleResultSerializer
        return InfluxDBAdmin._execute_query(query, parser)

    @staticmethod
    def show_queries():
        query = 'SHOW QUERIES'
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
    def show_users():
        query = 'SHOW USERS'
        parser = serializers.FlatFormattedSerieSerializer
        return InfluxDBAdmin._execute_query(query, parser)
