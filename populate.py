import arrow
import random
from influxable import Influxable, attributes
from influxable.measurement import Measurement

NB_YEARS = 5

client = Influxable()


class TemperatureMeasurement(Measurement):
    measurement_name = 'temperature'

    time = attributes.TimestampFieldAttribute(precision='s')
    phase = attributes.TagFieldAttribute()
    value = attributes.FloatFieldAttribute()


def populate():
    end_date = arrow.now('Europe/Paris').replace(hour=0, minute=0, second=0)
    start_date = end_date.shift(years=-NB_YEARS)
    date_range = arrow.Arrow.span_range('month', start_date, end_date)
    for current_start_month, current_end_month in date_range:
        points = []
        phasis = ['moon', 'sun']
        current_date = current_start_month
        while current_date <= current_end_month:
            points.append(TemperatureMeasurement(
                phase=random.choice(phasis),
                value=random.uniform(15.4, 28.7),
                time=current_date.timestamp,
            ))
            current_date = current_date.shift(minutes=1)
        TemperatureMeasurement.bulk_save(points)


if __name__ == '__main__':
    populate()
