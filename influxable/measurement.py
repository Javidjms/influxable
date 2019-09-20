from .attributes import BaseAttribute, GenericFieldAttribute, \
    TagFieldAttribute, TimestampFieldAttribute
from .db.query import Query, BulkInsertQuery
from .response import InfluxDBResponse
from .serializers import MeasurementPointSerializer


class MeasurementMeta(type):
    def __init__(cls, name, *args, **kwargs):
        super(MeasurementMeta, cls).__init__(name, *args, **kwargs)
        attribute_names = cls._get_attribute_names()
        cls._extend_attributes(attribute_names)

        get_query = cls._factory_get_query()
        setattr(cls, 'get_query', get_query)

    def __call__(cls, *args, **kwargs):
        setattr(cls, '_get_attributes', cls._get_attributes)
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
        def filter_func(x):
            return isinstance(variables[x], BaseAttribute)
        variables = cls.__dict__
        attribute_names = list(filter(filter_func, variables))
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

    def _extend_attributes(cls, attribute_names):
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


class Measurement(object, metaclass=MeasurementMeta):
    parser_class = MeasurementPointSerializer
    measurement_name = 'default'

    def __init__(self, **kwargs):
        self.check_attribute_values(**kwargs)
        self.clone_attributes()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def check_attribute_values(self, **kwargs):
        def filter_required_attributes(x):
            return not x.default and not x.is_nullable

        attributes = self._get_attributes()
        required_attributes = list(filter(
            filter_required_attributes,
            attributes,
        ))
        required_attributes_names = [
            r.attribute_name
            for r in required_attributes
        ]
        for key in required_attributes_names:
            if key not in kwargs:
                raise AttributeError('The field {} is not defined'.format(key))

    def clone_attributes(self):
        attributes = self._get_attributes()
        for attr in attributes:
            cloned_attribute = attr.clone()
            setattr(self, attr.ext_attribute_name, cloned_attribute)

    def dict(self):
        dict_values = {}
        attributes = self.get_attributes()
        for attr in attributes:
            dict_values[attr.attribute_name] = getattr(self, attr.attribute_name)
        return dict_values

    def get_attributes(self):
        def filter_func(x):
            return isinstance(x, BaseAttribute)
        variables = self.__dict__.values()
        attributes = list(filter(filter_func, variables))
        return attributes

    def get_attribute_names(self):
        attributes = self.get_attributes()
        attribute_names = [attr.attribute_name for attr in attributes]
        return attribute_names

    def get_ext_attribute_names(self):
        attributes = self.get_attributes()
        attribute_names = [attr.ext_attribute_name for attr in attributes]
        return attribute_names

    def get_timestamp_attributes(self):
        def filter_func(x):
            return isinstance(x, TimestampFieldAttribute)
        attributes = self.get_attributes()
        timestamp_attributes = list(filter(filter_func, attributes))
        return timestamp_attributes

    def get_prep_value(self):
        def factory_filter_func(cls):
            def filter_func(attr):
                return isinstance(attr, cls)
            return filter_func

        attributes = self.get_attributes()
        field_attributes = list(filter(
            factory_filter_func(GenericFieldAttribute),
            attributes,
        ))
        tag_attributes = list(filter(
            factory_filter_func(TagFieldAttribute),
            attributes,
        ))
        timestamp_attributes = list(filter(
            factory_filter_func(TimestampFieldAttribute),
            attributes,
        ))

        prep_value_groups = []
        attributes_groups = [field_attributes, tag_attributes, timestamp_attributes]
        for attr_group in attributes_groups:
            prep_value_group = []
            for attr in attr_group:
                attr_prep_value = attr.get_prep_value()
                attr_name = attr.name or attr.attribute_name
                prep_value = '{}={}'.format(attr_name, attr_prep_value)
                prep_value_group.append(prep_value)
            str_prep_value_group = ','.join(prep_value_group)
            prep_value_groups.append(str_prep_value_group)

        prep_value_groups[0] = ','.join([self.measurement_name] + [prep_value_groups[0]])
        final_prep_value = ' '.join(prep_value_groups)
        return final_prep_value

    def items(self):
        return self.dict().items()

    @staticmethod
    def bulk_save(points):
        str_points = '\n'.join([point.get_prep_value() for point in points])
        return BulkInsertQuery(str_points).execute()
