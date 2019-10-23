import json
import pandas as pd
from influxable import attributes, serializers
from influxable.db import RawQuery
from influxable.measurement import Measurement
from influxable.response import InfluxDBResponse


class TestSerializer:
    def create_measurement_class(self):
        class MySampleMeasurement(Measurement):
            measurement_name = 'mysamplemeasurement'
            time = attributes.TimestampFieldAttribute(precision="s")
            value = attributes.IntegerFieldAttribute()
        measurement_cls = MySampleMeasurement
        return measurement_cls

    def execute_query(self, query):
        response = RawQuery(query).execute()
        influx_response = InfluxDBResponse(response)
        return influx_response

    def execute_sample_query(self):
        query = 'SHOW DATABASES'
        influx_response = self.execute_query(query)
        return influx_response

    def test_base_serializer_success(self):
        influx_response = self.execute_sample_query()
        serializer = serializers.BaseSerializer(influx_response)
        data = serializer.convert()
        assert isinstance(data, dict)
        assert 'results' in data

    def test_json_serializer_success(self):
        influx_response = self.execute_sample_query()
        serializer = serializers.JsonSerializer(influx_response)
        data = serializer.convert()
        json_data = json.loads(data)
        assert isinstance(data, str)
        assert json_data is not None

    def test_formatted_serie_serializer_success(self):
        influx_response = self.execute_sample_query()
        serializer = serializers.FormattedSerieSerializer(influx_response)
        data = serializer.convert()
        assert isinstance(data, list)
        assert len(data) == 1
        assert 'databases' in data[0]

    def test_flat_formatted_serie_serializer_success(self):
        influx_response = self.execute_sample_query()
        serializer = serializers.FlatFormattedSerieSerializer(influx_response)
        data = serializer.convert()
        assert isinstance(data, list)
        for d in data:
            assert isinstance(d, dict)

    def test_flat_simple_result_serializer_success(self):
        influx_response = self.execute_sample_query()
        serializer = serializers.FlatSimpleResultSerializer(influx_response)
        data = serializer.convert()
        assert isinstance(data, list)
        for d in data:
            assert isinstance(d, str)

    def test_pandas_serializer_success(self):
        influx_response = self.execute_sample_query()
        serializer = serializers.PandasSerializer(influx_response)
        data = serializer.convert()
        assert type(data) == pd.DataFrame

    def test_measurement_serializer_success(self):
        measurement_cls = self.create_measurement_class()
        points = measurement_cls\
            .get_query()\
            .limit(10)\
            .evaluate()

        assert isinstance(points, list)
        for p in points:
            assert isinstance(p, measurement_cls)
