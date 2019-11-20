import os
import humps
from pathlib import Path
from influxable import Influxable, attributes
from influxable.db import InfluxDBAdmin
from jinja2 import Environment, FileSystemLoader

client = Influxable()

TEMPLATE_FILE_NAME = 'auto_generated_measurement.py.jinja'


def get_classname(cls):
    return cls.__name__


def pascalize(str):
    return humps.pascalize(str)


FIELD_TYPE_ATTRIBUTE_MAP = {
    'integer': get_classname(attributes.IntegerFieldAttribute),
    'float': get_classname(attributes.FloatFieldAttribute),
    'boolean': get_classname(attributes.BooleanFieldAttribute),
    'string': get_classname(attributes.StringFieldAttribute),
}

TAG_CLASSNAME = get_classname(attributes.TagFieldAttribute)


class AutoGenerateMeasurement():
    @staticmethod
    def get_template_path():
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        template_folder_path = Path(current_dir_path) / '../templates/'
        return template_folder_path.resolve().as_posix()

    @staticmethod
    def retrieve_measurement_fields():
        all_measurements_fields = {}
        measurements_field_keys = InfluxDBAdmin.show_field_keys()
        measurements_tag_keys = InfluxDBAdmin.show_tag_keys()

        for measurement_field_keys in measurements_field_keys:
            measurement_name, fields = list(measurement_field_keys.items())[0]
            all_measurements_fields.setdefault(measurement_name, [])
            for field in fields:
                field_key = field['fieldKey']
                field_type = field['fieldType']
                field_tuple = (field_key, FIELD_TYPE_ATTRIBUTE_MAP[field_type])
                all_measurements_fields[measurement_name].append(field_tuple)

        for measurement_tag_keys in measurements_tag_keys:
            measurement_name, tags = list(measurement_tag_keys.items())[0]
            all_measurements_fields.setdefault(measurement_name, [])
            for tag in tags:
                tag_key = tag['tagKey']
                tag_tuple = (tag_key, TAG_CLASSNAME)
                all_measurements_fields[measurement_name].append(tag_tuple)

        return all_measurements_fields

    @staticmethod
    def run(*args, **kwargs):
        output_file_name = kwargs.get('output_file_name')
        measurements_fields = AutoGenerateMeasurement.retrieve_measurement_fields()
        template_path = AutoGenerateMeasurement.get_template_path()

        j2_env = Environment(
            loader=FileSystemLoader(template_path),
            trim_blocks=True,
        )

        j2_env.filters['pascalize'] = pascalize

        rendered_template = j2_env\
            .get_template(TEMPLATE_FILE_NAME)\
            .render(measurements_fields=measurements_fields)

        with open(output_file_name, "wb") as f:
            f.write(str.encode(rendered_template))
