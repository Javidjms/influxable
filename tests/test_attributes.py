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

