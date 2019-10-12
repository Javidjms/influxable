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

    def test_show_series_cardinality_with_exact_success(self):
        res = InfluxDBAdmin.show_series_cardinality(exact=True)
        assert res is not None

    def test_show_tag_key_cardinality_success(self):
        res = InfluxDBAdmin.show_tag_key_cardinality()
        assert res is not None

    def test_show_tag_key_cardinality_with_exact_success(self):
        res = InfluxDBAdmin.show_tag_key_cardinality(exact=True)
        assert res is not None

    def test_show_tag_values_cardinality_success(self):
        res = InfluxDBAdmin.show_tag_values_cardinality('phase')
        assert res is not None

    def test_show_tag_values_cardinality_with_exact_success(self):
        res = InfluxDBAdmin.show_tag_values_cardinality('phase', exact=True)
        assert res is not None

    def test_show_continuous_queries_success(self):
        res = InfluxDBAdmin.show_continuous_queries()
        assert res is not None

    def test_show_diagnostics_success(self):
        res = InfluxDBAdmin.show_diagnostics()
        assert res is not None

    def test_show_field_keys_success(self):
        res = InfluxDBAdmin.show_field_keys()
        assert res is not None

    def test_show_field_keys_with_measurement_success(self):
        res = InfluxDBAdmin.show_field_keys('param1')
        assert res is not None

    def test_show_field_keys_with_multiple_measurement_success(self):
        res = InfluxDBAdmin.show_field_keys('param1', 'param2')
        assert res is not None

    def test_show_grants_success(self):
        res = InfluxDBAdmin.show_grants('admin')
        assert res is not None

