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
