import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .attributes import BaseAttribute, GenericFieldAttribute, \
    TagFieldAttribute, TimestampFieldAttribute
from .db.query import Query, BulkInsertQuery
from .response import InfluxDBResponse
from .serializers import MeasurementPointSerializer
from .exceptions import InfluxDBAttributeValueError

EXTENDED_ATTRIBUTE_PREFIX_NAME = '__attribute__'

TEMPLATE_FILE_NAME = 'simple_measurement.py.jinja'


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
                def __init__(self):
                    super(MeasurementQuery, self).__init__()

                def format(self, result, parser_class=cls.parser_class):
                    return parser_class(result, cls).convert()

                def evaluate(self, parser_class=cls.parser_class):
                    result = InfluxDBResponse(self.execute())
                    result.raise_if_error()
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
            ext_attribute_name = EXTENDED_ATTRIBUTE_PREFIX_NAME + attribute_name
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
        self.fill_values(**kwargs)

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
                raise InfluxDBAttributeValueError(
                    'The attribute \'{}\' cannot be nullable'.format(key)
                )

    def clone_attributes(self):
        attributes = self._get_attributes()
        for attr in attributes:
            cloned_attribute = attr.clone()
            cloned_attribute.attribute_name = attr.attribute_name
            cloned_attribute.ext_attribute_name = attr.ext_attribute_name
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
        attributes_groups = [tag_attributes, field_attributes, timestamp_attributes]
        for attr_group in attributes_groups:
            prep_value_group = []
            for attr in attr_group:
                attr_prep_value = attr.get_prep_value()
                attr_name = attr.name or attr.attribute_name
                if not isinstance(attr, TimestampFieldAttribute):
                    prep_value = '{}={}'.format(attr_name, attr_prep_value)
                else:
                    prep_value = '{}'.format(attr_prep_value)
                prep_value_group.append(prep_value)
            str_prep_value_group = ','.join(prep_value_group)
            prep_value_groups.append(str_prep_value_group)

        if prep_value_groups[0]:
            prep_value_groups[0] = ','.join(
                [self.measurement_name] + [prep_value_groups[0]]
            )
        else:
            prep_value_groups[0] = self.measurement_name
        final_prep_value = ' '.join(prep_value_groups)
        return final_prep_value

    def fill_values(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except Exception as err:
            print('key', key)
            msg = '<\'{key}\'> : {msg}'.format(key=key, msg=err)
            raise InfluxDBAttributeValueError(msg)

    def items(self):
        return self.dict().items()

    @staticmethod
    def bulk_save(points):
        if not isinstance(points, list):
            raise InfluxDBAttributeValueError('points must be a list')
        str_points = ''
        for point in points:
            if not isinstance(point, Measurement):
                raise InfluxDBAttributeValueError(
                    'type of point must be Measurement'
                )
            prep_value = point.get_prep_value()
            str_points += prep_value
            str_points += '\n'
        return BulkInsertQuery(str_points).execute()


def SimpleMeasurement(measurement_name, field_names, tag_names=[]):
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    template_folder_path = Path(current_dir_path) / './templates/'
    template_folder_path = template_folder_path.resolve().as_posix()

    j2_env = Environment(
        loader=FileSystemLoader(template_folder_path),
        trim_blocks=True,
    )
    rendered_template = j2_env\
        .get_template(TEMPLATE_FILE_NAME)\
        .render(
            measurement_name=measurement_name,
            field_names=field_names,
            tag_names=tag_names,
        )

    exec(rendered_template)
    anonymous_measurement = locals().get('AnonymousMeasurement')
    return anonymous_measurement
