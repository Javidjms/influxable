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
