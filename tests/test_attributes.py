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

