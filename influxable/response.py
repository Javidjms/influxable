class InfluxDBResponse:
    def __init__(self, raw_json):
        self._raw_json = raw_json

    @property
    def raw(self):
        return self._raw_json

    @property
    def main_serie(self):
        series = self.series
        if len(series):
            return series[0]
        return None

    @property
    def series(self):
        if 'results' in self.raw:
            results = self.raw['results']
            if len(results):
                result = results[0]
                if 'series' in result:
                    return [InfluxDBSerieResponse(s) for s in result['series']]
        return []


class InfluxDBSerieResponse:
    def __init__(self, json_serie):
        self._raw_json_serie = json_serie

    @property
    def raw(self):
        return self._raw_json_serie

    @property
    def columns(self):
        return self._raw_json_serie["columns"]

    @property
    def name(self):
        return self._raw_json_serie.get("name", "default")

    @property
    def values(self):
        return self._raw_json_serie["values"]


class InfluxDBErrorResponse:
    def __init__(self, raw_json):
        self._raw_json = raw_json

    @property
    def raw(self):
        return self._raw_json

    @property
    def error(self):
        return self.raw['error']
