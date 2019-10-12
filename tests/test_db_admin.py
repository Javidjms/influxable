from influxable.db import InfluxDBAdmin, Field


class TestDBAdminShowCommand:
    def test_show_field_key_cardinality_success(self):
        res = InfluxDBAdmin.show_field_key_cardinality()
        assert res is not None

    def test_show_field_key_cardinality_with_exact_success(self):
        res = InfluxDBAdmin.show_field_key_cardinality(exact=True)
        assert res is not None

    def test_show_measurement_cardinality_success(self):
        res = InfluxDBAdmin.show_measurement_cardinality()
        assert res is not None

    def test_show_measurement_cardinality_with_exact_success(self):
        res = InfluxDBAdmin.show_measurement_cardinality(exact=True)
        assert res is not None

    def test_show_series_cardinality_success(self):
        res = InfluxDBAdmin.show_series_cardinality()
        assert res is not None

