import json
import itertools
class DefaultSerializer:
    def __init__(self, response):
        self.response = response

    def convert(self):
        return self.response


class JsonSerializer(DefaultSerializer):
    def convert(self):
        return json.dumps(self.response.raw)


class FormattedSerieSerializer(DefaultSerializer):
    def convert(self):
        formatted_series = []
        series = self.response.series
        for serie in series:
            name = serie.name
            columns = serie.columns
            values = serie.values
            formatted_values = [dict(zip(columns, v)) for v in values]
            formatted_series.append({name: formatted_values})
        return formatted_series


class FlatFormattedSerieSerializer(FormattedSerieSerializer):
    def convert(self):
        formatted_series = super().convert()
        if len(formatted_series) == 1:
            main_serie = formatted_series[0]
            flat_main_serie = list(main_serie.values())[0]
            return flat_main_serie
        return []


class FlatSimpleResultSerializer(DefaultSerializer):
    def convert(self):
        serie = self.response.main_serie
        values = serie.values
        flatten_serie = list(itertools.chain(*values))
        return flatten_serie


