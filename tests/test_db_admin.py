from influxable.db import InfluxDBAdmin, Field


class TestDBAdminShowCommand:
    def test_show_field_key_cardinality_success(self):
        res = InfluxDBAdmin.show_field_key_cardinality()
        assert res is not None

