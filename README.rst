Influxable
==========

A lightweight python ORM / ODM / Client for InfluxDB

Note
----

This project is currently in development.

A better documentation and testing scripts will be added in the next release.

Dependencies
------------

-  Python 3 (Tested with Python 3.7.3)

-  InfluxDB (Tested with InfluxDB 1.5.4)

Installation
------------

The package is available in pypi. You can install it via pip :

::

    pip install influxable

Getting started
---------------

Connection
~~~~~~~~~~

You can set your environment variable for the connection of InfluxDB in order to override the default values :

::

    INFLUXDB_URL=http://localhost:8086
    INFLUXDB_DATABASE_NAME=default

    #Optional
    INFLUXDB_USER=admin
    INFLUXDB_PASSWORD=changme

Then you just have to import the influxable package and create an instance of *Influxable* :

.. code:: python

    from influxable import Influxable

    client = Influxable()

You can also set connection variable in *Influxable* constructor :

.. code:: python

    # Without authentication

    client = Influxable(
        base_url='http://localhost:8086',
        database_name='default',
    )

    # With authentication

    client = Influxable(
        base_url='http://localhost:8086',
        database_name='default',
        user='admin',
        password='changeme',
    )

Measurement
~~~~~~~~~~~

.. code:: python

    from influxable import attributes
    from influxable.measurement import Measurement

    class TemperatureMeasurement(Measurement):
        parser_class = MeasurementPointSerializer # Default
        measurement_name = 'temperature'

        time = attributes.TimestampFieldAttribute()
        phase = attributes.TagFieldAttribute()
        value = attributes.FloatFieldAttribute()

Fields :

-  GenericFieldAttribute (IntegerFieldAttribute, FloatFieldAttribute, StringFieldAttribute, BooleanFieldAttribute)

-  TagFieldAttribute

-  TimestampFieldAttribute, DateTimeFieldAttribute

Parser Classes :

-  MeasurementPointSerializer (default)

-  JsonSerializer

-  FormattedSerieSerializer

-  FlatFormattedSerieSerializer

-  FlatSimpleResultSerializer

-  PandasSerializer

Instanciation
~~~~~~~~~~~~~

.. code:: python

    point = TemperatureMeasurement(
      time=1568970572,
      phase="HOT",
      value=23.5,
    )

Query
~~~~~

You can query with *Measurement.get\_query()* :

.. code:: python

    from influxable.db.criteria import Field

    points = TemperatureMeasurement\
      .get_query()\
      .select('phase', 'value')\
      .where(
         Field('value') > 15.2,
         Field('value') < 30.5,
      )\
      .limit(100)
      .evaluate()

You can also query with *Query* :

.. code:: python

    from influxable.db.query import Query
    from influxable.db.criteria import Field

    points = Query()\
      .select('phase', 'value')\
      .from_measurements('temperature')\
      .where(
         Field('value') > 15.2,
         Field('value') < 30.5,
      )\
      .limit(100)
      .execute()

Saving Data
~~~~~~~~~~~

You can create data by using *Measurement.bulk\_save()*

.. code:: python

    points = [
        TemperatureMeasurement(phase="HOT", value=30, time=1463289075),
        TemperatureMeasurement(phase="COLD", value=10, time=1463289275),
    ]
    TemperatureMeasurement.bulk_save(points)

You can also create data with *BulkInsertQuery*

.. code:: python

    str_query = '''
    temperature,phase=HOT value=30 1463289075000000000
    temperature,phase=COLD value=10 1463289275000000000
    '''

    raw_query = BulkInsertQuery(str_query)
    res = raw_query.execute()

Supporting
----------

Feel free to post issues your feedback or if you reach a problem with influxable library.

If you want to contribute, please use the pull requests section.

Authors
-------

Javid Mougamadou javidjms0@gmail.com
