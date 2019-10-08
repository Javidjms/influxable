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

    def test_check_attributes_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls(time=1570481055, value=10)
        assert instance is not None

    def test_check_attributes_failed(self):
        with pytest.raises(exceptions.InfluxDBAttributeValueError):
            measurement_cls = self.create_measurement_class_with_required()
            measurement_cls()

    def test_clone_attributes_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls()
        cls_attrs = instance._get_attributes()
        for attr in cls_attrs:
            cloned_attribute = getattr(instance, attr.ext_attribute_name)
            assert attr != cloned_attribute

    def test_fill_values_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls(time=1570481055, value=10)
        assert instance.time == D(1570481055)
        assert instance.value == 10

    def test_fill_values_failed(self):
        with pytest.raises(exceptions.InfluxDBAttributeValueError):
            measurement_cls = self.create_measurement_class_with_required()
            measurement_cls(time='1570481055', value="S")

    def test_dict_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls(time=1570481055, value=10)
        assert instance.dict() == {'time': D('1570481055'), 'value': 10}

    def test_get_attributes_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls(time=1570481055, value=10)
        attrs = instance.get_attributes()
        for attr in attrs:
            assert isinstance(attr, attributes.BaseAttribute)

    def test_get_attribute_names_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls(time=1570481055, value=10)
        attr_names = instance.get_attribute_names()
        assert attr_names == ['time', 'value']

    def test_get_ext_attribute_names_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls(time=1570481055, value=10)
        attr_names = instance.get_ext_attribute_names()
        assert attr_names == ['__attribute__time', '__attribute__value']

    def test_get_timestamp_attributes_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls(time=1570481055, value=10)
        time_attrs = instance.get_timestamp_attributes()
        for attr in time_attrs:
            assert isinstance(attr, attributes.TimestampFieldAttribute)

    def test_get_prep_value_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls(time=1570481055, value=10)
        prep_value = instance.get_prep_value()
        assert prep_value == 'mysamplemeasurement value=10i 1570481055000000000'

    def test_items_success(self):
        measurement_cls = self.create_measurement_class()
        instance = measurement_cls(time=1570481055, value=10)
        items = {'time': D('1570481055'), 'value': 10}.items()
        assert instance.items() == items

    def test_bulk_success(self):
        measurement_cls = self.create_measurement_class()
        measurements = [
            measurement_cls(time=1570481055, value=10),
            measurement_cls(time=1570481065, value=20),
            measurement_cls(time=1570481075, value=30),
        ]
        res = measurement_cls.bulk_save(measurements)
        assert res is True

    def test_bulk_fail_1(self):
        with pytest.raises(exceptions.InfluxDBAttributeValueError):
            measurement_cls = self.create_measurement_class()
            measurements = True
            measurement_cls.bulk_save(measurements)

    def test_bulk_fail_2(self):
        with pytest.raises(exceptions.InfluxDBAttributeValueError):
            measurement_cls = self.create_measurement_class()
            measurements = [True, True, True]
            measurement_cls.bulk_save(measurements)
