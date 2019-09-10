class InfluxDBResponse:
    def __init__(self, raw_json):
        self._raw_json = raw_json

    @property
    def raw(self):
        return self._raw_json

class InfluxDBResponseSerie:
    def __init__(self, json_serie):
        self._raw_json_serie = json_serie

    @property
    def raw(self):
        return self._raw_json_serie
