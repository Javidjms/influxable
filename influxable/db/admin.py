from .query import RawQuery


class InfluxDBAdmin:
    @staticmethod
    def show_databases():
        return RawQuery('SHOW DATABASES').execute()
