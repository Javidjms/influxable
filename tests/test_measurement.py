import pytest
from decimal import Decimal as D
from influxable import attributes, exceptions
from influxable.db import Query
from influxable.measurement import Measurement, MeasurementMeta
from influxable.serializers import MeasurementPointSerializer


class TestMeasurement:
    def create_measurement_class(self):
        class MySampleMeasurement(Measurement):
            measurement_name = 'mysamplemeasurement'
            time = attributes.TimestampFieldAttribute(precision="s")
            value = attributes.IntegerFieldAttribute()
        measurement_cls = MySampleMeasurement
        return measurement_cls

    def create_measurement_class_with_required(self):
        class MySampleMeasurement(Measurement):
            measurement_name = 'mysamplemeasurement'
            time = attributes.TimestampFieldAttribute()
            value = attributes.IntegerFieldAttribute(is_nullable=False)
        measurement_cls = MySampleMeasurement
        return measurement_cls

    def test_meta_check_type_success(self):
        measurement_cls = self.create_measurement_class()
        assert measurement_cls.__class__ == MeasurementMeta

    def test_meta_get_attribute_names_success(self):
        measurement_cls = self.create_measurement_class()
        attr_names = measurement_cls._get_attribute_names()
        assert attr_names == ['__attribute__time', '__attribute__value']

