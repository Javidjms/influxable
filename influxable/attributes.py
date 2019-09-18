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

