from influxable import settings


class TestSettings:
    def check_if_variable_exist(self, variable_name):
        return hasattr(settings, variable_name)
