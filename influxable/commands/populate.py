import arrow
import random
from influxable import Influxable, attributes
from influxable.measurement import Measurement

client = Influxable.get_instance()


def get_populate_measurement(name):
    class PopulateMeasurement(Measurement):
        measurement_name = name

        time = attributes.TimestampFieldAttribute(precision='s')
        phase = attributes.TagFieldAttribute()
        value = attributes.FloatFieldAttribute()
    return PopulateMeasurement


class Populate():
    @staticmethod
    def run(*args, **kwargs):
        measurement_name = kwargs.get('measurement_name')
        PopulateMeasurement = get_populate_measurement(measurement_name)

        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        interval_delay = kwargs.get('interval_delay')

        tags = kwargs.get('tags')
        max_count = kwargs.get('max_count_of_values', None)

        min_value = kwargs.get('min_value')
        max_value = kwargs.get('max_value')
        value_range = (min_value, max_value)
        date_range = list(arrow.Arrow.span_range('month', start_date, end_date))
        date_range.reverse()

        count = 0
        for current_start_month, current_end_month in date_range:
            if max_count is not None and count > max_count:
                break

            points = []
            current_date = current_end_month
            while current_date >= current_start_month:

                if max_count is not None and count > max_count:
                    break
                points.append(PopulateMeasurement(
                    phase=random.choice(tags),
                    value=random.uniform(*value_range),
                    time=current_date.timestamp,
                ))
                current_date = current_date.shift(minutes=-interval_delay)
                count += 1
            PopulateMeasurement.bulk_save(points)
