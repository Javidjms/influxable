import click
from influxable.commands.auto_generate import AutoGenerateMeasurement


@click.group()
def main(*args, **kwargs):
    pass


@main.command(name='autogenerate')
@click.option(
    '-o',
    '--output',
    'output_file_name',
    default='auto_generate_measurement.py',
    help='name of the output file',
)
def auto_generate(*args, **kwargs):
    """
    This command will automatically generate measurement classes.
    """
    AutoGenerateMeasurement.run(*args, **kwargs)
