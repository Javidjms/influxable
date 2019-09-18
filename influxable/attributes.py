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
