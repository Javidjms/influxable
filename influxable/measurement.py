from .attributes import BaseAttribute, GenericFieldAttribute, \
    TagFieldAttribute, TimestampFieldAttribute
from .db.query import Query, BulkInsertQuery
from .response import InfluxDBResponse
from .serializers import MeasurementPointSerializer


class MeasurementMeta(type):
    def __init__(cls, name, *args, **kwargs):
        super(MeasurementMeta, cls).__init__(name, *args, **kwargs)
        attribute_names = cls._get_attribute_names()
        cls._extend_fields(attribute_names)

        get_query = cls._factory_get_query()
        setattr(cls, 'get_query', get_query)

    def __call__(cls, *args, **kwargs):
        instance = type.__call__(cls, *args, **kwargs)
        return instance

    def _factory_get_query(cls):
        def get_query():
            class MeasurementQuery(Query):
                def format(self, result, parser_class=cls.parser_class):
                    return parser_class(result, cls).convert()

                def evaluate(self, parser_class=cls.parser_class):
                    result = InfluxDBResponse(self.execute())
                    formatted_result = self.format(result, parser_class)
                    return formatted_result
            return MeasurementQuery().from_measurements(cls.measurement_name)
        return get_query

    def _get_attribute_names(cls):
        attributes = cls._get_attributes()
        attribute_names = [attr.attribute_name for attr in attributes]
        return attribute_names

    def _get_attributes(cls):
        def filter_func(x):
            return isinstance(x, BaseAttribute)
        variables = cls.__dict__.values()
        attributes = list(filter(filter_func, variables))
        return attributes

    def _get_timestamp_attributes(cls):
        def filter_func(x):
            return isinstance(x, TimestampFieldAttribute)
        attributes = cls._get_attributes()
        timestamp_attributes = list(filter(filter_func, attributes))
        return timestamp_attributes

    def _extend_fields(cls, attribute_names):
        def generate_getter_and_setter(attr_name):
            def getx(self):
                attribute_field = getattr(self, attr_name)
                return attribute_field.get_internal_value()

            def setx(self, value):
                attribute_field = getattr(self, attr_name)
                attribute_field.set_internal_value(value)
            return getx, setx

        for attribute_name in attribute_names:
            ext_attribute_name = '_extended_' + attribute_name
            attribute_field = getattr(cls, attribute_name)
            attribute_field.attribute_name = attribute_name
            attribute_field.ext_attribute_name = ext_attribute_name

            getx, setx = generate_getter_and_setter(ext_attribute_name)
            prop = property(getx, setx)
            setattr(cls, ext_attribute_name, attribute_field)
            setattr(cls, attribute_name, prop)


