from functools import lru_cache
from .criteria import Criteria
from .function import aggregations
from ..response import InfluxDBResponse
from ..serializers import BaseSerializer
from .. import Influxable, exceptions


class RawQuery:
    def __init__(self, str_query=''):
        self.str_query = str_query

    def execute(self):
        return self.raw_response

    @property
    def query(self):
        return self.str_query

    @property
    def raw_response(self):
        return self._resolve()

    @lru_cache(maxsize=None)
    def _resolve(self, *args, **kwargs):
        instance = Influxable.get_instance()
        return instance.execute_query(query=self.str_query, method='post')


class SelectQueryClause:
    def __init__(self):
        super(SelectQueryClause, self).__init__()
        self.select_clause = 'SELECT {fields}'
        self.selected_fields = []
        self.default_selected_fields = '*'

    def validate_field(self, field):
        if not isinstance(field, str):
            msg = 'field type must be <str>'
            raise exceptions.InfluxDBInvalidTypeError(msg)

    def select(self, *fields):
        selected_fields = []
        for field in fields:
            if not hasattr(field, 'evaluate'):
                self.validate_field(field)
                evaluated_field = str(field)
            else:
                evaluated_field = field.evaluate()
            selected_fields.append(evaluated_field)
        self.selected_fields = selected_fields
        return self

    def _prepare_select_clause(self):
        if len(self.selected_fields):
            joined_fields = ','.join(self.selected_fields)
        else:
            joined_fields = self.default_selected_fields
        return self.select_clause.format(fields=joined_fields)


class IntoQueryClause:
    def __init__(self):
        super(IntoQueryClause, self).__init__()
        self.into_clause = 'INTO {measurement}'
        self.selected_into_measurement = None

    def validate_measurement(self, measurement):
        if not isinstance(measurement, str):
            msg = 'measurement type must be <str>'
            raise exceptions.InfluxDBInvalidTypeError(msg)

    def into(self, measurement):
        self.validate_measurement(measurement)
        self.selected_into_measurement = measurement
        return self

    def _prepare_into_clause(self):
        into_clause = ''
        if self.selected_into_measurement is not None:
            into_clause = self.into_clause.format(
                measurement=self.selected_into_measurement,
            )
        return into_clause


        self.selected_measurements = 'default'
        self.limit_value = None
        self.slimit_value = None
        self.offset_value = None
        self.soffset_value = None

    def from_measurements(self, *measurements):
        quoted_measurements = ['"{}"'.format(m) for m in measurements]
        self.selected_measurements = ', '.join(quoted_measurements)
        return self

    def select(self, *fields):
        evaluated_fields = []
        for f in fields:
            evaluated_field = f.evaluate() if hasattr(f, 'evaluate') else f
            evaluated_fields.append(evaluated_field)
        self.selected_fields = ', '.join(evaluated_fields)
        return self

    def where(self, *criteria):
        self.selected_criteria = list(criteria)
        return self

    def limit(self, value):
        self.limit_value = value
        return self

    def slimit(self, value):
        self.slimit_value = value
        return self

    def offset(self, value):
        self.offset_value = value
        return self

    def soffset(self, value):
        self.soffset_value = value
        return self

    def count(self, value='*'):
        return self.select(aggregations.Count(value))

    def distinct(self, value='*'):
        return self.select(aggregations.Distinct(value))

    def integral(self, value='*'):
        return self.select(aggregations.Integral(value))

    def mean(self, value='*'):
        return self.select(aggregations.Mean(value))

    def median(self, value='*'):
        return self.select(aggregations.Median(value))

    def mode(self, value='*'):
        return self.select(aggregations.Mode(value))

    def spread(self, value='*'):
        return self.select(aggregations.Spread(value))

    def std_dev(self, value='*'):
        return self.select(aggregations.StdDev(value))

    def sum(self, value='*'):
        return self.select(aggregations.Sum(value))

    def _prepare_query(self):
        select_clause = self.select_clause.format(fields=self.selected_fields)
        from_clause = self.from_clause.format(measurements=self.selected_measurements)
        prepared_query = self.initial_query.format(
            select_clause=select_clause,
            from_clause=from_clause,
        )
        if len(self.selected_criteria):
            criteria = [c.evaluate() for c in self.selected_criteria]
            eval_criteria = ' AND '.join(criteria)
            self.where_clause = self.where_clause.format(criteria=eval_criteria)
            prepared_query += self.where_clause
        if self.limit_value is not None:
            self.limit_clause = ' LIMIT {}'.format(self.limit_value)
            prepared_query += self.limit_clause
        if self.offset_value is not None:
            self.offset_clause = ' OFFSET {}'.format(self.offset_value)
            prepared_query += self.offset_clause
        if self.slimit_value is not None:
            self.slimit_clause = ' SLIMIT {}'.format(self.slimit_value)
            prepared_query += self.slimit_clause
        if self.soffset_value is not None:
            self.soffset_clause = ' SOFFSET {}'.format(self.soffset_value)
            prepared_query += self.soffset_clause
        print('prepared_query', prepared_query)
        return prepared_query

    def execute(self):
        prepared_query = self._prepare_query()
        self.str_query = prepared_query
        return super().execute()

    def format(self, result, parser_class=BaseSerializer, **kwargs):
        return parser_class(result, **kwargs).convert()

    def evaluate(self, parser_class=BaseSerializer, **kwargs):
        result = InfluxDBResponse(self.execute())
        result.raise_if_error()
        formatted_result = self.format(result, parser_class, **kwargs)
        return formatted_result


class BulkInsertQuery(RawQuery):
    @lru_cache(maxsize=None)
    def _resolve(self, *args, **kwargs):
        instance = Influxable.get_instance()
        return instance.write_points(points=self.str_query)
