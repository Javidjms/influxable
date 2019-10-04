import arrow
import pytest
from datetime import datetime
from decimal import Decimal as D
from influxable import attributes, exceptions


class TestBaseAttribute:
    def test_clean_success(self):
        base_attr = attributes.BaseAttribute()
        base_attr._value = 5
        base_attr.clean(5)
        value = base_attr.get_internal_value()
        assert value == 5

    def test_clean_with_none_value_success(self):
        base_attr = attributes.BaseAttribute()
        base_attr.clean(None)
        value = base_attr.get_internal_value()
        assert value is None

    def test_clean_with_default_value_success(self):
        base_attr = attributes.BaseAttribute(default=10)
        base_attr.clean(None)
        value = base_attr.get_internal_value()
        assert value == 10

    def test_clone_success(self):
        base_attr = attributes.BaseAttribute()
        cloned_attr = base_attr.clone()
        assert base_attr != cloned_attr

    def test_clone_with_value_success(self):
        base_attr = attributes.BaseAttribute()
        base_attr._value = 5
        cloned_attr = base_attr.clone()
        value = base_attr.get_internal_value()
        cloned_value = cloned_attr.get_internal_value()
        assert base_attr != cloned_attr
        assert value == cloned_value

    def test_get_internal_value_success(self):
        base_attr = attributes.BaseAttribute()
        base_attr._value = 5
        assert base_attr._value == 5
        assert base_attr.value == 5
        assert base_attr.get_internal_value() == 5

    def test_get_prep_value_success(self):
        base_attr = attributes.BaseAttribute()
        base_attr._value = 5
        assert base_attr.get_prep_value() == base_attr.to_influx(5)

    def test_get_name_success(self):
        base_attr = attributes.BaseAttribute(name='my_field')
        assert base_attr.attribute_name == 'my_field'
        assert base_attr.name == 'my_field'

    def test_reset_success(self):
        base_attr = attributes.BaseAttribute()
        base_attr._value = 5
        base_attr.reset()
        assert base_attr.get_internal_value() is None

    def test_set_internal_value_success(self):
        base_attr = attributes.BaseAttribute()
        base_attr.set_internal_value(5)
        assert base_attr.get_internal_value() == 5
        base_attr.set_internal_value(True)
        assert base_attr.get_internal_value() is True
        base_attr.set_internal_value('hello')
        assert base_attr.get_internal_value() == 'hello'
        base_attr.set_internal_value(None)
        assert base_attr.get_internal_value() is None

    def test_validate_is_nullable_fail(self):
        with pytest.raises(exceptions.InfluxDBAttributeValueError):
            base_attr = attributes.BaseAttribute(is_nullable=False)
            base_attr.set_internal_value(None)

