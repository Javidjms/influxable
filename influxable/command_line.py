import arrow
import click
from influxable.commands.auto_generate import AutoGenerateMeasurement
from influxable.commands.populate import Populate


DEFAULT_OUTPUT_FILE_NAME = 'auto_generate_measurement.py'

DEFAULT_INTERVAL_DELAY = 30
DEFAULT_NB_YEARS_RANGE = 5
DEFAULT_POPULATE_MIN_VALUE = 10
DEFAULT_POPULATE_MAX_VALUE = 30
DEFAULT_MEASUREMENT_NAME = 'populate_temperature'
DEFAULT_TAGS = ['moon', 'sun']


def get_default_start_date():
    end_date = arrow.now('Europe/Paris').replace(hour=0, minute=0, second=0)
    start_date = end_date.shift(years=-DEFAULT_NB_YEARS_RANGE)
    return start_date.format('YYYY-MM-DDTHH:mm:ss')


def get_default_end_date():
    end_date = arrow.now('Europe/Paris').replace(hour=0, minute=0, second=0)
    return end_date.format('YYYY-MM-DDTHH:mm:ss')


@click.group()
def main(*args, **kwargs):
    pass


@main.command(name='autogenerate')
@click.option(
    '-o',
    '--output',
    'output_file_name',
    default=DEFAULT_OUTPUT_FILE_NAME,
    help='name of the output file',
)
def auto_generate(*args, **kwargs):
    """
    This command will automatically generate measurement classes.
    """
    AutoGenerateMeasurement.run(*args, **kwargs)


@main.command(name='populate')
@click.option(
    '--min_value',
    'min_value',
    type=int,
    default=DEFAULT_POPULATE_MIN_VALUE,
    help='minimum value for the populate range',
)
@click.option(
    '--max_value',
    'max_value',
    type=int,
    default=DEFAULT_POPULATE_MAX_VALUE,
    help='maximum value for the populate range',
)
@click.option(
    '-s',
    '--start_date',
    'start_date',
    type=click.DateTime(),
    default=get_default_start_date(),
    help='the start date range of populate values',
)
@click.option(
    '-e',
    '--end_date',
    'end_date',
    type=click.DateTime(),
    default=get_default_end_date(),
    help='the end date range of populate values',
)
@click.option(
    '-m',
    '--max_count_of_values',
    'max_count_of_values',
    type=int,
    default=None,
    help='maximum limit of added values count',
)
@click.option(
    '-id',
    '--interval_delay',
    'interval_delay',
    type=int,
    default=DEFAULT_INTERVAL_DELAY,
    help='maximum value for the populate range ',
)
@click.option(
    '-t',
    '--tags',
    'tags',
    multiple=True,
    default=DEFAULT_TAGS,
    help='list of tags for the populate',
)
@click.option(
    '-mn',
    '--measurement_name',
    'measurement_name',
    default=DEFAULT_MEASUREMENT_NAME,
    help='name of the populate measurement',
)
def populate(*args, **kwargs):
    """
    This command will exectute the populate command.
    """
    Populate.run(*args, **kwargs)
