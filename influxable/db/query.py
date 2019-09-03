from functools import lru_cache
from .. import Influxable


class RawQuery:
    def __init__(self, str_query):
        self.str_query = str_query

    def execute(self):
        return self.raw_response

    @property
    def raw_response(self):
        return self._resolve()

    @lru_cache(maxsize=None)
    def _resolve(self, *args, **kwargs):
        instance = Influxable.get_instance()
        return instance.execute_query(query=self.str_query, method='post')


class Query(RawQuery):
    def __init__(self):
        self.initial_query = '{select_clause} {from_clause}'
        self.from_clause = 'FROM {measurements}'
        self.select_clause = 'SELECT {fields}'
        self.where_clause = ' WHERE {criteria}'
        self.selected_fields = '*'
        self.selected_criteria = []
        self.selected_measurements = 'default'
        self.limit_value = None
        self.slimit_value = None
        self.offset_value = None

    def from_measurements(self, *measurements):
        quoted_measurements = ['"{}"'.format(m) for m in measurements]
        self.selected_measurements = ', '.join(quoted_measurements)
        return self

    def select(self, *fields):
        self.selected_fields = ', '.join(fields)
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
        if self.limit_value:
            self.limit_clause = ' LIMIT {}'.format(self.limit_value)
            prepared_query += self.limit_clause
        if self.offset_value:
            self.offset_clause = ' OFFSET {}'.format(self.offset_value)
            prepared_query += self.offset_clause
        if self.slimit_value:
            self.slimit_clause = ' SLIMIT {}'.format(self.slimit_value)
            prepared_query += self.slimit_clause
        print('prepared_query', prepared_query)
        return prepared_query

    def execute(self):
        prepared_query = self._prepare_query()
        self.str_query = prepared_query
        return super().execute()
