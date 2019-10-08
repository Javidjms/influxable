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

    def test_meta_check_has_query_attr_success(self):
        measurement_cls = self.create_measurement_class()
        assert hasattr(measurement_cls, 'get_query')

    def test_meta_create_instance_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls()
        assert isinstance(instance, measurement_cls)
        assert hasattr(instance, 'get_query')
        assert hasattr(instance, '_get_attributes')

    def test_factory_get_query_success(self):
        measurement_cls = self.create_measurement_class()
        query = measurement_cls.get_query()
        assert isinstance(query, Query)

    def test_meta_get_attributes_success(self):
        measurement_cls = self.create_measurement_class()
        attrs = measurement_cls._get_attributes()
        for attr in attrs:
            assert isinstance(attr, attributes.BaseAttribute)

    def test_meta_get_timestamp_attribute_success(self):
        measurement_cls = self.create_measurement_class()
        timestamp_attrs = measurement_cls._get_timestamp_attributes()
        for attr in timestamp_attrs:
            assert isinstance(attr, attributes.TimestampFieldAttribute)

    def test_measurement_name_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls()
        assert measurement_cls.measurement_name == 'mysamplemeasurement'
        assert instance.measurement_name == 'mysamplemeasurement'

    def test_parser_class_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls()
        assert measurement_cls.parser_class == MeasurementPointSerializer
        assert instance.parser_class == MeasurementPointSerializer

    def test_extend_attributes_success(self):
        measurement_cls = self.create_measurement_class()
        attrs = measurement_cls._get_attributes()
        for attr in attrs:
            attribute_name = attr.attribute_name
            ext_attribute_name = attr.ext_attribute_name
            assert hasattr(measurement_cls, attribute_name)
            assert hasattr(measurement_cls, ext_attribute_name)
            prop = getattr(measurement_cls, attribute_name)
            attr_field = getattr(measurement_cls, ext_attribute_name)
            assert isinstance(attr_field, attributes.BaseAttribute)
            assert isinstance(prop, property)

