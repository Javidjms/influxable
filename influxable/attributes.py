import arrow
from decimal import Decimal as D
from .helpers.utils import inv


class TimestampPrecision:
    HOURS = 'h'
    MICROSECONDS = 'u'
    MILLISECONDS = 'ms'
    MINUTES = 'm'
    NANOSECONDS = 'ns'
    SECONDS = 's'


TIMESTAMP_CONVERT_RATIO = {
    TimestampPrecision.HOURS: inv(60 * 60),
    TimestampPrecision.MICROSECONDS: 1 * 1000 * 1000,
    TimestampPrecision.MILLISECONDS: 1000,
    TimestampPrecision.MINUTES: inv(60),
    TimestampPrecision.NANOSECONDS: 1 * 1000 * 1000 * 1000,
    TimestampPrecision.SECONDS: 1,
}


class BaseAttribute:
    def __init__(self, **kwargs):
        self._value = None
        self.raw_value = None
        self.attribute_name = kwargs.get('name', None)
        self.default = kwargs.get('default', None)
        self.enforce_cast = kwargs.get('enforce_cast', True)
        self.is_nullable = kwargs.get('is_nullable', True)

    def clean(self, value):
        if value is None and self.default is not None:
            self._value = self.default
        elif value is None:
            self._value = None

    def clone(self):
        cls = self.__class__
        instance = cls(**self.__dict__)
        if self._value is not None:
            instance.set_internal_value(self._value)
        return instance

    def get_internal_value(self):
        return self._value

    def get_prep_value(self):
        prep_value = self.to_influx(self._value)
        return prep_value

    @property
    def name(self):
        return self.attribute_name

    def to_influx(self, value):
        return str(value)

    def to_python(self, value):
        return str(value)

    def reset(self):
        self._value = None

    def set_internal_value(self, value):
        self.validate(value)
        self.raw_value = value
        if value is not None:
            try:
                self._value = self.to_python(value)
            except ValueError as exception:
                if self.enforce_cast:
                    raise exception
                self._value = value
        self.clean(value)

    def validate(self, value):
        if value is None and self.default is None and not self.is_nullable:
            raise ValueError('This field cannot be nullable')

    @property
    def value(self):
        return self.get_internal_value()


class GenericFieldAttribute(BaseAttribute):
    pass


class IntegerFieldAttribute(GenericFieldAttribute):
    def __init__(self, **kwargs):
        super(IntegerFieldAttribute, self).__init__(**kwargs)
        self.min_value = kwargs.get('min_value', None)
        self.max_value = kwargs.get('max_value', None)

    def to_influx(self, value):
        str_value = str(value)
        return "{}i".format(str_value)

    def to_python(self, value):
        return int(value)

    def validate(self, value):
        super(IntegerFieldAttribute, self).validate(value)
        if value is not None and self.min_value is not None and int(value) < self.min_value:
            raise ValueError('The value must be greater than the min_value')
        if value is not None and self.max_value is not None and int(value) > self.max_value:
            raise ValueError('The value must be lower than the max_value')


class FloatFieldAttribute(IntegerFieldAttribute):
    def __init__(self, **kwargs):
        super(FloatFieldAttribute, self).__init__(**kwargs)
        self.max_nb_decimals = kwargs.get('max_nb_decimals', None)

    def clean(self, value):
        super(FloatFieldAttribute, self).clean(value)
        if self.max_nb_decimals is not None:
            precision = '.' + '0' * (self.max_nb_decimals - 1) + '1'
            self._value = self.to_python(value).quantize(D(precision))

    def to_influx(self, value):
        str_value = str(value)
        return str_value

    def to_python(self, value):
        return D(value)

    def validate(self, value):
        super(FloatFieldAttribute, self).validate(value)
        if self.max_nb_decimals is not None and not isinstance(self.max_nb_decimals, int):
            raise ValueError('max_nb_decimals must be integer')
        if self.max_nb_decimals is not None and self.max_nb_decimals <= 0:
            raise ValueError('max_nb_decimals must be positive')


class StringFieldAttribute(GenericFieldAttribute):
    def __init__(self, **kwargs):
        super(StringFieldAttribute, self).__init__(**kwargs)
        self.choices = kwargs.get('choices', None)
        self.max_length = kwargs.get('max_length', None)

    def to_influx(self, value):
        str_value = str(value)
        return "\'{}\'".format(str_value)

    def to_python(self, value):
        return str(value)

    def validate(self, value):
        super(StringFieldAttribute, self).validate(value)
        if self.choices is not None and not isinstance(self.choices, list):
            raise ValueError('choices must be a list')
        if self.choices is not None and not any(
            [isinstance(c, str) for c in self.choices]
        ):
            raise ValueError('choices items must be a string')
        if self.choices is not None and value not in self.choices:
            raise ValueError('The value is not refered in choices')
        if self.max_length is not None and not isinstance(self.max_length, int):
            raise ValueError('max_length must be integer')
        if self.max_length is not None and self.max_length <= 0:
            raise ValueError('max_length must be positive')
        if self.max_length is not None and len(str(value)) > self.max_length:
            raise ValueError('the string length must be lower than the max_length')


class BooleanFieldAttribute(GenericFieldAttribute):
    def to_influx(self, value):
        str_value = str(value).lower()
        return str_value

    def to_python(self, value):
        return bool(value)


class TagFieldAttribute(BaseAttribute):
    pass


class TimestampFieldAttribute(BaseAttribute):
    def __init__(self, **kwargs):
        super(TimestampFieldAttribute, self).__init__(**kwargs)
        self.auto_now = kwargs.get('auto_now', True)
        self.precision = kwargs.get('precision', 'ns')

    def clean(self, value):
        super(TimestampFieldAttribute, self).clean(value)
        if value is None and self.auto_now:
            timestamp = arrow.now().timestamp
            self._value = self.to_python(timestamp)
            self.formatted_timestamp = self.convert_to_nanoseconds(timestamp)
        elif value:
            self.formatted_timestamp = self.convert_to_nanoseconds(value)
        else:
            self.formatted_timestamp = None

    def convert_to_nanoseconds(self, timestamp):
        precision = TimestampPrecision.NANOSECONDS
        return self.convert_to_precision(timestamp, precision)

    def convert_to_precision(self, timestamp, precision):
        convert_ratio = TIMESTAMP_CONVERT_RATIO[precision]
        return D(timestamp) * convert_ratio

    def to_influx(self, value):
        timestamp = D(self.formatted_timestamp)
        str_value = str(timestamp)
        return "{}".format(str_value)

    def to_python(self, value):
        timestamp = D(value)
        return self.convert_to_precision(timestamp, self.precision)

    def validate(self, value):
        super(TimestampFieldAttribute, self).validate(value)
        if self.precision not in TIMESTAMP_CONVERT_RATIO:
            raise ValueError('precision must be one of [ns,u,ms,s,m,h]')


class DateTimeFieldAttribute(TimestampFieldAttribute):
    def __init__(self, **kwargs):
        super(DateTimeFieldAttribute, self).__init__(**kwargs)
        self.str_format = kwargs.get('str_format', 'YYYY-MM-DD HH:mm:ss ZZ')

    def clean(self, value):
        super(DateTimeFieldAttribute, self).clean(value)
        if value is None and self.auto_now:
            timestamp = arrow.now().datetime
            self._value = self.to_python(timestamp)

    def get_internal_value(self):
        return arrow.get(self._value).format(self.str_format)

    def to_influx(self, value):
        timestamp = arrow.get(value).timestamp
        nanoseconds = self.convert_to_nanoseconds(timestamp)
        str_value = str(nanoseconds)
        return "{}".format(str_value)

    def to_python(self, value):
        datetime = arrow.get(value).datetime
        return datetime
