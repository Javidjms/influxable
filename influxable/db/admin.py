from .query import RawQuery


class InfluxDBAdmin:
    @staticmethod
    def show_databases():
        return RawQuery('SHOW DATABASES').execute()

    @staticmethod
    def show_measurements():
        return RawQuery('SHOW MEASUREMENTS').execute()

    @staticmethod
    def show_queries():
        return RawQuery('SHOW QUERIES').execute()

    @staticmethod
    def show_series():
        return RawQuery('SHOW SERIES').execute()

    @staticmethod
    def show_stats():
        return RawQuery('SHOW STATS').execute()

    @staticmethod
    def show_users():
        return RawQuery('SHOW USERS').execute()
