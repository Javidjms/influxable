.. figure:: ./artwork/logo.svg
   :alt:

Influxable
==========

|pypi version| |build status| |code coverage| |license: MIT|

A lightweight python ORM / ODM / Client for InfluxDB

Table of Contents
-----------------

-  `Note <#note>`__
-  `Genesis <#genesis>`__
-  `Changelog <#changelog>`__
-  `Features <#features>`__
-  `Dependencies <#dependencies>`__
-  `Installation <#installation>`__
-  `Getting started <#getting-started>`__

   -  `Connection <#connection>`__
   -  `Measurement <#measurement>`__
   -  `Simple Measurement <#simple-measurement>`__
   -  `Instanciation <#instanciation>`__
   -  `Query <#query>`__
   -  `Saving Data <#saving-data>`__

-  `Auto Generation of Measurements <#auto-generation-of-measurements>`__
-  `Influxable commands <#influxable-commands>`__
-  `Influxable API <#influxable-api>`__

   -  `Influxable Class <#influxable-class>`__
   -  `InfluxDBApi Class <#influxdbapi-class>`__
   -  `Connection Class <#connection-class>`__
   -  `Measurement Class <#measurement-class>`__
   -  `Attributes <#attributes>`__
   -  `InfluxDBResponse <#influxdbresponse>`__
   -  `Serializers <#serializers>`__
   -  `Raw Query <#raw-query>`__
   -  `Query Class <#query-class>`__
   -  `Query aggregations function <#query-aggregations-function>`__
   -  `Query selectors function <#query-selectors-function>`__
   -  `Query transformations function <#query-transformations-function>`__
   -  `InfluxDBAdmin <#influxdbadmin>`__
   -  `Exceptions <#exceptions>`__

-  `Testing <#testing>`__
-  `Supporting <#supporting>`__
-  `Versioning <#versioning>`__
-  `Contributors <#contributors>`__
-  `Credits <#credits>`__
-  `References <#references>`__
-  `License <#license>`__

Note
----

This project is currently in development.

A better documentation and testing scripts will be added in the next release.

Genesis
-------

I worked on a project with InfluxDB. I needed to build an API for InfluxDB and to plug with Python libraries (scipy, pandas, etc ...).

That's why I decided to create this repository in order to deal with InfluxDB in a smooth way and to manipulate Python object.

Changelog
---------

1.3.0
~~~~~

-  Add *group\_by()* method for *GROUP BY tags* instructions

-  Add *range()* method for *GROUP BY time()* instructions

-  Add *into()* method for *INTO* instructions

-  Add *tz()* method

1.2.1
~~~~~

-  Handle chinese characters.

Features
--------

-  Add automation for measurement class generation (command: *autogenerate*)

-  Admin commands allowing to manage the database (ex: *create\_user()*, *show\_series()*).

-  Measurement class allowing to make queries in order to fetch/save points (ex: *Measurement.where()*, *Measurement.bulk\_save()*).

-  Group by commands

-  Different serializers for easy data manipulation (ex: *PandasSerializer*).

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

    from influxable import attributes, serializers
    from influxable.measurement import Measurement

    class TemperatureMeasurement(Measurement):
        parser_class = serializers.MeasurementPointSerializer # Default
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

Simple Measurement
~~~~~~~~~~~~~~~~~~

.. code:: python

    from influxable.measurement import SimpleMeasurement

    my_measurement = SimpleMeasurement('temperature', ['value'], ['phase'])

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

    from influxable.db import Field

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

    from influxable.db import Query, Field

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
        TemperatureMeasurement(phase="HOT",value=10,time=1463289075),
        TemperatureMeasurement(phase="COLD",value=10,time=1463289076),
    ]
    TemperatureMeasurement.bulk_save(points)

You can also create data with *BulkInsertQuery*

.. code:: python

    str_query = '''
    temperature,phase=HOT value=10 1463289075000000000
    temperature,phase=COLD value=10 1463289076000000000
    '''

    raw_query = BulkInsertQuery(str_query)
    res = raw_query.execute()

Auto Generation of Measurements
-------------------------------

You can automatically generate measurement classes file with the bash command *autogenerate*

.. code:: bash

    influxable autogenerate #(default to auto_generate_measurement.py)
    influxable autogenerate -o measurement.py

Here is the output generated file :

.. code:: python

    # auto_generate_measurement.py

    from influxable import attributes
    from influxable.measurement import Measurement


    class CpuMeasurement(Measurement):
        measurement_name = 'cpu'

        time = attributes.TimestampFieldAttribute(precision='s')
        value = attributes.FloatFieldAttribute()
        host = attributes.TagFieldAttribute()

Influxable commands
-------------------

-  *autogenerate* : automatic generation of measurement classes

.. code:: bash

    influxable autogenerate #(default to auto_generate_measurement.py)
    influxable autogenerate -o measurement.py

-  *populate* : create a measurement filled with a set of random data

.. code:: bash

    influxable populate
    influxable populate --min_value 5 --max_value 35 -s 2011-01-01T00:00:00 -id 1
    influxable populate --help

Influxable API
--------------

Influxable Class
~~~~~~~~~~~~~~~~

The Influxable main app class is a singleton. You can access it via the method *Influxable.get\_instance()*

\_\_init\_\_():
^^^^^^^^^^^^^^^

-  base\_url : url to connect to the InfluxDB server (default = 'http://localhost:8086')

-  user : authentication user name (default = 'admin')

-  password : authentication user password (default = 'changeme')

-  database\_name : name of the database (default = 'default')

create\_connection() -> Connection:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  base\_url : url to connect to the InfluxDB server (default = 'http://localhost:8086')

-  user : authentication user name (default = 'admin')

-  password : authentication user password (default = 'changeme')

-  database\_name : name of the database (default = 'default')

ping() -> bool:
^^^^^^^^^^^^^^^

-  verbose : enables verbose mode (default = True)

execute\_query() -> json():
^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  query: influxdb query to execute
-  method: http method of the request (default='get')
-  chunked: if enabled, responses will be chunked by series or by every 10,000 points (default=False)
-  epoch: specified precision of the timestamp [ns,u,µ,ms,s,m,h] (default='ns')
-  pretty: if enadble, the json response is pretty-printed (default=False)

write\_points() -> bool:
^^^^^^^^^^^^^^^^^^^^^^^^

-  points: data to write in InfluxDB line protocol format

ex: mymeas,mytag1=1 value=21 1463689680000000000

-  precision: specified precision of the timestamp [ns,u,µ,ms,s,m,h] (default='ns')
-  consistency: sets the write consistency for the point [any,one,quorum,all] (default='all')
-  retention\_policy\_name: sets the target retention policy for the write (default='DEFAULT')

InfluxDBApi Class
~~~~~~~~~~~~~~~~~

get\_debug\_requests() -> bool:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  request : instance of InfluxDBRequest

get\_debug\_vars() -> bool:
^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  request : instance of InfluxDBRequest

ping() -> bool:
^^^^^^^^^^^^^^^

-  request : instance of InfluxDBRequest

-  verbose : enables verbose mode (default = True)

execute\_query() -> json():
^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  request : instance of InfluxDBRequest
-  query: influxdb query to execute
-  method: http method of the request (default='get')
-  chunked: if enabled, responses will be chunked by series or by every 10,000 points (default=False)
-  epoch: specified precision of the timestamp [ns,u,µ,ms,s,m,h] (default='ns')
-  pretty: if enadble, the json response is pretty-printed (default=False)

write\_points() -> bool:
^^^^^^^^^^^^^^^^^^^^^^^^

-  request : instance of InfluxDBRequest

-  points: data to write in InfluxDB line protocol format

ex: mymeas,mytag1=1 value=21 1463689680000000000

-  precision: specified precision of the timestamp [ns,u,µ,ms,s,m,h] (default='ns')
-  consistency: sets the write consistency for the point [any,one,quorum,all] (default='all')
-  retention\_policy\_name: sets the target retention policy for the write (default='DEFAULT')

Connection Class
~~~~~~~~~~~~~~~~

\_\_init\_\_():
^^^^^^^^^^^^^^^

-  base\_url : url to connect to the InfluxDB server (default = 'http://localhost:8086')

-  user : authentication user name (default = 'admin')

-  password : authentication user password (default = 'changeme')

-  database\_name : name of the database (default = 'default')

create() -> Connection:
^^^^^^^^^^^^^^^^^^^^^^^

-  base\_url : url to connect to the InfluxDB server (default = 'http://localhost:8086')

-  user : authentication user name (default = 'admin')

-  password : authentication user password (default = 'changeme')

-  database\_name : name of the database (default = 'default')

Measurement Class
~~~~~~~~~~~~~~~~~

fields
^^^^^^

Must be an instance of class located in *influxable.attributes*

-  GenericFieldAttribute

-  IntegerFieldAttribute

-  FloatFieldAttribute

-  StringFieldAttribute

-  BooleanFieldAttribute

-  TagFieldAttribute

-  TimestampFieldAttribute

-  DateTimeFieldAttribute

Example :

.. code:: python

    class MySensorMeasurement(Measurement):
        measurement_name = 'mysensor'

        time = TimestampFieldAttribute(auto_now=True, precision='s')
        phase = TagFieldAttribute()
        value = IntegerFieldAttribute()

parser\_class
^^^^^^^^^^^^^

Must be a class of *influxable.serializers* :

-  MeasurementPointSerializer (default)

-  JsonSerializer

-  FormattedSerieSerializer

-  FlatFormattedSerieSerializer

-  FlatSimpleResultSerializer

-  PandasSerializer

measurement\_name
^^^^^^^^^^^^^^^^^

Name of the measurement in InfluxDB

\_\_init\_\_():
^^^^^^^^^^^^^^^

Set the attribute value of a Measurement

Example

.. code:: python

    point = MySensorMeasurement(value=0.5, phase="MOON")

get\_query() -> Query:
^^^^^^^^^^^^^^^^^^^^^^

Return an instance of Query which

Example

.. code:: python

    points = MySensorMeasurement\
      .get_query()\
      .select()\
      .where()\
      .limit()\
      .evaluate()

dict()
^^^^^^

Return a dict of the point values

Example

.. code:: python

    point = MySensorMeasurement(value=0.5, phase="MOON")

    point.dict()

    # {'time': Decimal('1568970572'), 'phase': 'MOON', 'value': 0.5}

items()
^^^^^^^

Return an item list of the point values

Example

.. code:: python

    point = MySensorMeasurement(value=0.5, phase="MOON")

    point.items()

    # dict_items([('time', Decimal('1568970572')), ('phase', 'MOON'), ('value', 0.5)])

bulk\_save()
^^^^^^^^^^^^

Save a list of measurement point

.. code:: python

    points = [
        MySensorMeasurement(phase="moon",value=5,time=1463489075),
        MySensorMeasurement(phase="moon",value=7,time=1463489076),
        MySensorMeasurement(phase="sun",value=8,time=1463489077),
    ]
    MySensorMeasurement.bulk_save(points)

Attributes
~~~~~~~~~~

GenericFieldAttribute
^^^^^^^^^^^^^^^^^^^^^

-  attribute\_name : real name of the measurement attribute in database

-  default : set a default value if it is not filled at the instanciation

-  is\_nullable : if False, it will raise an error if the value is null (default=True)

-  enforce\_cast : if False, it will not raise an error when the value has not the desired type without casting (default=True).

.. code:: python

    class MySensorMeasurement(Measurement):
        measurement_name = 'mysensor'

        temperature_value = GenericFieldAttribute(
          attribute_name="temp_v1",
          default="15",
          is_nullable=True,
          enforce_cast=False,
        )

IntegerFieldAttribute
^^^^^^^^^^^^^^^^^^^^^

-  min\_value : an error is raised if the value is less than the min\_value

-  max\_value : an error is raised if the value is greater than the max\_value

-  attribute\_name : real name of the measurement attribute in database

-  default : set a default value if it is not filled at the instanciation

-  is\_nullable : if False, it will raise an error if the value is null (default=True)

-  enforce\_cast : if False, it will not raise an error when the value has not the desired type without casting (default=True).

.. code:: python

    class MySensorMeasurement(Measurement):
        measurement_name = 'mysensor'

        temperature_value = IntegerFieldAttribute(
          min_value=10,
          max_value=30,
        )

FloatFieldAttribute
^^^^^^^^^^^^^^^^^^^

-  max\_nb\_decimals : set the maximal number of decimals to display

-  min\_value : an error is raised if the value is less than the min\_value

-  max\_value : an error is raised if the value is greater than the max\_value

-  attribute\_name : real name of the measurement attribute in database

-  default : set a default value if it is not filled at the instanciation

-  is\_nullable : if False, it will raise an error if the value is null (default=True)

-  enforce\_cast : if False, it will not raise an error when the value has not the desired type without casting (default=True).

.. code:: python

    class MySensorMeasurement(Measurement):
        measurement_name = 'mysensor'

        value = FloatFieldAttribute(
          max_nb_decimals=5,
        )

StringFieldAttribute
^^^^^^^^^^^^^^^^^^^^

-  choices : an error is raised if the value is not in the list of string options

-  max\_length : an error is raised if the string value length is greater than the max\_length

-  attribute\_name : real name of the measurement attribute in database

-  default : set a default value if it is not filled at the instanciation

-  is\_nullable : if False, it will raise an error if the value is null (default=True)

-  enforce\_cast : if False, it will not raise an error when the value has not the desired type without casting (default=True).

.. code:: python

    class MySensorMeasurement(Measurement):
        measurement_name = 'mysensor'

        position = FloatFieldAttribute(
          choices=['first', 'last'],
          max_length=7,
        )

BooleanFieldAttribute
^^^^^^^^^^^^^^^^^^^^^

-  attribute\_name : real name of the measurement attribute in database

-  default : set a default value if it is not filled at the instanciation

-  is\_nullable : if False, it will raise an error if the value is null (default=True)

-  enforce\_cast : if False, it will not raise an error when the value has not the desired type without casting (default=True).

.. code:: python

    class MySensorMeasurement(Measurement):
        measurement_name = 'mysensor'

        is_marked = BooleanFieldAttribute(
          default=False,
        )

TagFieldAttribute
^^^^^^^^^^^^^^^^^

-  attribute\_name : real name of the measurement attribute in database

-  default : set a default value if it is not filled at the instanciation

-  is\_nullable : if False, it will raise an error if the value is null (default=True)

-  enforce\_cast : if False, it will not raise an error when the value has not the desired type without casting (default=True).

.. code:: python

    class MySensorMeasurement(Measurement):
        measurement_name = 'mysensor'

        phase = TagFieldAttribute(
          default='MOON',
        )

TimestampFieldAttribute
^^^^^^^^^^^^^^^^^^^^^^^

-  auto\_now : Set automatically the current date (default=False)

-  precision : Set the timestamp precision which must be one of [ns,u,ms,s,m,h] (default= 'ns')

-  attribute\_name : real name of the measurement attribute in database

-  default : set a default value if it is not filled at the instanciation

-  is\_nullable : if False, it will raise an error if the value is null (default=True)

-  enforce\_cast : if False, it will not raise an error when the value has not the desired type without casting (default=True).

.. code:: python

    class MySensorMeasurement(Measurement):
        measurement_name = 'mysensor'

        time = TimestampFieldAttribute(
          auto_now=True,
          precision='s',
        )

DateTimeFieldAttribute
^^^^^^^^^^^^^^^^^^^^^^

-  str\_format : Set the arrow format of the timestamp to display (default: "YYYY-MM-DD HH:mm:ss")

-  auto\_now : Set automatically the current date

-  precision : Set the timestamp precision which must be one of [ns,u,ms,s,m,h]

-  attribute\_name : real name of the measurement attribute in database

-  default : set a default value if it is not filled at the instanciation

-  is\_nullable : if False, it will raise an error if the value is null (default=True)

-  enforce\_cast : if False, it will not raise an error when the value has not the desired type without casting (default=True).

.. code:: python

    class MySensorMeasurement(Measurement):
        measurement_name = 'mysensor'

        date = DateTimeFieldAttribute(
          attribute_name='time',
          auto_now=True,
          str_format='YYYY-MM-DD',
        )

InfluxDBResponse
~~~~~~~~~~~~~~~~

\_\_init\_\_():
^^^^^^^^^^^^^^^

-  raw\_json : the raw json response object

raw
^^^

Return the raw\_json value

main\_serie
^^^^^^^^^^^

Return the first serie from the *series* field in the raw\_json value

series
^^^^^^

Return the *series* field in the raw\_json value

error
^^^^^

Return the *error* field in the raw\_json value

Example of json raw response :

.. code:: python

    {
       "results":[
          {
             "statement_id":0,
             "series":[
                {
                   "name":"mymeas",
                   "columns":[
                      "time",
                      "myfield",
                      "mytag1",
                      "mytag2"
                   ],
                   "values":[
                      [
                         "2017-03-01T00:16:18Z",
                         33.1,
                         null,
                         null
                      ],
                      [
                         "2017-03-01T00:17:18Z",
                         12.4,
                         "12",
                         "14"
                      ]
                   ]
                }
             ]
          }
       ]
    }

Serializers
~~~~~~~~~~~

Serializers can be used in *parser\_class* field of *Measurement* class.

.. code:: python

    class MySensorMeasurement(Measurement):
        measurement_name = 'mysensor'
        parser_class = serializers.BaseSerializer

It allow to change the output response format of a influxb request

.. code:: python

    # res is formatted with BaseSerializer
    res = MySensorMeasurement.get_query().limit(10).evaluate()

BaseSerializer
^^^^^^^^^^^^^^

.. code:: python

    # res is formatted with BaseSerializer
    res
    {'results': [{'statement_id': 0, 'series': [{'name': 'mysamplemeasurement', 'columns': ['time', 'value'], 'values': [[1570481055000000000, 10], [1570481065000000000, 20], [1570481075000000000, 30]]}]}]}

JsonSerializer
^^^^^^^^^^^^^^

.. code:: python

    # res is formatted with JsonSerializer
    res
    '{"results": [{"statement_id": 0, "series": [{"name": "mysamplemeasurement", "columns": ["time", "value"], "values": [[1570481055000000000, 10], [1570481065000000000, 20], [1570481075000000000, 30]]}]}]}'

FormattedSerieSerializer
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    # res is formatted with FormattedSerieSerializer
    res
    [{'mysamplemeasurement': [{'time': 1570481055000000000, 'value': 10}, {'time': 1570481065000000000, 'value': 20}, {'time': 1570481075000000000, 'value': 30}]}]

FlatFormattedSerieSerializer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    # res is formatted with FlatFormattedSerieSerializer
    [{'time': 1570481055000000000, 'value': 10}, {'time': 1570481065000000000, 'value': 20}, {'time': 1570481075000000000, 'value': 30}]

FlatSimpleResultSerializer
^^^^^^^^^^^^^^^^^^^^^^^^^^

This serializer is used only when the result set contains only one column

.. code:: python

    res = InfluxDBAdmin.show_databases()

    # res is formatted with FlatSimpleResultSerializer
    res
    ['_internal', 'example', 'test', 'telegraf', 'mydb', ...]

FlatSingleValueSerializer
^^^^^^^^^^^^^^^^^^^^^^^^^

This serializer is used only when the result set contains only one value

.. code:: python

    res = InfluxDBAdmin.show_measurement_cardinality()

    # res is formatted with FlatSingleValueSerializer
    res
    2

PandasSerializer
^^^^^^^^^^^^^^^^

.. code:: python

    # res is formatted with PandasSerializer
    res                   time  value
    0  1570481055000000000     10
    1  1570481065000000000     20
    2  1570481075000000000     30

MeasurementPointSerializer
^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the default serializer class for Measurement

.. code:: python

    [<MySensorMeasurement object at 0x7f49a16227f0>, <MySensorMeasurement object at 0x7f49a16228d0>, <MySensorMeasurement object at 0x7f49a1622438>]

Raw Query
~~~~~~~~~

-  str\_query

Example :

.. code:: python

    from influxable.db import RawQuery
    str_query = 'SHOW DATABASES'
    res = RawQuery(str_query).execute()

.. code:: python

    from influxable.db import RawQuery
    str_query = 'SELECT * FROM temperature LIMIT 10'
    res = RawQuery(str_query).execute()

Query Class
~~~~~~~~~~~

You can generate an instance of Query via the initial Query constructor or from a measurement.

Example :

.. code:: python

    from influxable.db import Query
    query = Query()
    ...

.. code:: python

    query = MySensorMeasurement.get_query()
    ...

Methods :

from\_measurements()
^^^^^^^^^^^^^^^^^^^^

-  \*measurements

Example :

.. code:: python

    query = Query()\
      .from_measurements('measurement1', 'measurement2')

Render :

.. code:: sql

    FROM measurement1, measurement2

select()
^^^^^^^^

-  \*fields

Example :

.. code:: python

    query = Query()\
      .select('param1', 'param2')\
      .from_measurements('measurement1')

Render :

.. code:: sql

    SELECT value, phase

where()
^^^^^^^

-  \*criteria

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .select('param1', 'param2')\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )

Render :

.. code:: sql

    WHERE param1 > 800 AND param1 < 900

limit()
^^^^^^^

-  value

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .select('param1', 'param2')\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .limit(10)

Render :

.. code:: sql

    LIMIT 10

slimit()
^^^^^^^^

-  value

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .select('param1', 'param2')\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .limit(10)\
      .slimit(5)

Render :

.. code:: sql

    SLIMIT 5

offset()
^^^^^^^^

-  value

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .select('param1', 'param2')\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .offset(10)

Render :

.. code:: sql

    OFFSET 10

soffset()
^^^^^^^^^

-  value

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .select('param1', 'param2')\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .offset(10)\
      .soffset(5)

Render :

.. code:: sql

    SOFFSET 5

into()
^^^^^^

-  \*measurement

Example :

.. code:: python

    query = Query()\
      .select('param1')\
      .from_measurements('measurement1')\
      .into('measurement2')

Render :

.. code:: sql

    SELECT param1 INTO measurement2 FROM measurement1

asc()
^^^^^

Example :

.. code:: python

    query = Query()\
      .select('param1')\
      .from_measurements('measurement1')\
      .asc()

Render :

.. code:: sql

    SELECT param1 FROM measurement1 ORDER BY ASC

desc()
^^^^^^

Example :

.. code:: python

    query = Query()\
      .select('param1')\
      .from_measurements('measurement1')\
      .desc()

Render :

.. code:: sql

    SELECT param1 FROM measurement1 ORDER BY DESC

tz()
^^^^

Example :

.. code:: python

    query = Query()\
      .select('param1')\
      .from_measurements('measurement1')\
      .tz('Europe/Paris')

Render :

.. code:: sql

    SELECT param1 FROM measurement1 tz('Europe/Paris')

group\_by()
^^^^^^^^^^^

-  \*tags

Example :

.. code:: python

    query = Query()\
      .select('param1')\
      .from_measurements('measurement1')\
      .group_by('tag_1')

Render :

.. code:: sql

    SELECT param1 FROM measurement1 GROUP BY tag_1

range\_by()
^^^^^^^^^^^

-  \*interval
-  \*shift
-  \*fill
-  \*tags

Example :

.. code:: python

    query = Query()\
      .select('param1')\
      .from_measurements('measurement1')\
      .range_by('12s', shift='1d', tags=['tag1'], fill=3)

Render :

.. code:: sql

    SELECT param1 FROM measurement1 GROUP BY time(12s,1d),tag1 fill(3)'

execute()
^^^^^^^^^

Execute the query and return the response

Example :

.. code:: python

    from influxable.db import Query, Field
    res = Query()\
      .select('param1', 'param2')\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .execute()
    res

Result :

.. code:: python

    {'results': [{'statement_id': 0, 'series': [{'name': 'measurement1', 'columns': ['time', 'value'], 'values': [[1570481055000000000, 10], [1570481065000000000, 20], [1570481075000000000, 30]]}]}]}

evaluate()
^^^^^^^^^^

Execute the query and return the serialized response

-  parser\_class (default=BaseSerializer for Query and MeasurementPointSerializer for Measurement)

Example with Query :

.. code:: python

    from influxable.db import Query, Field
    res = Query()\
      .select('param1', 'param2')\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .evaluate()
    res

Result :

.. code:: python

    {'results': [{'statement_id': 0, 'series': [{'name': 'measurement1', 'columns': ['time', 'value'], 'values': [[1570481055000000000, 10], [1570481065000000000, 20], [1570481075000000000, 30]]}]}]}

Example with Measurement :

.. code:: python

    from influxable.db import Field
    points = MySensorMeasurement.get_query()
      .select('param1', 'param2')\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .evaluate()
    points

Result :

.. code:: python

    [<MySensorMeasurement object at 0x7f49a16227f0>, <MySensorMeasurement object at 0x7f49a16228d0>, <MySensorMeasurement object at 0x7f49a1622438>]

count()
^^^^^^^

-  value (default='\*')

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .count()

Render :

.. code:: sql

    SELECT COUNT(*)

distinct()
^^^^^^^^^^

-  value (default='\*')

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .distinct()

Render :

.. code:: sql

    SELECT DISTINCT(*)

integral()
^^^^^^^^^^

-  value (default='\*')

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .integral()

Render :

.. code:: sql

    SELECT INTEGRAL(*)

mean()
^^^^^^

-  value (default='\*')

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .mean()

Render :

.. code:: sql

    SELECT MEAN(*)

median()
^^^^^^^^

-  value (default='\*')

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .median()

Render :

.. code:: sql

    SELECT MEDIAN(*)

mode()
^^^^^^

-  value (default='\*')

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .mode()

Render :

.. code:: sql

    SELECT MODE(*)

spread()
^^^^^^^^

-  value (default='\*')

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .spread()

Render :

.. code:: sql

    SELECT SPREAD(*)

std\_dev()
^^^^^^^^^^

-  value (default='\*')

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .std_dev()

Render :

.. code:: sql

    SELECT STDDEV(*)

sum()
^^^^^

-  value (default='\*')

Example :

.. code:: python

    from influxable.db import Query, Field
    query = Query()\
      .from_measurements('measurement1')\
      .where(
          Field('param1') > 800,
          Field('param1') < 900,
      )\
      .sum()

Render :

.. code:: sql

    SELECT SUM(*)

Query aggregations function
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage :

.. code:: python

    from influxable.db.function import aggregations
    res = Query()\
        .select(aggregations.Sum('value'))\
        .from_measurements('param1')\
        .execute()

Count
^^^^^

Distinct
^^^^^^^^

Integral
^^^^^^^^

Mean
^^^^

Median
^^^^^^

Mode
^^^^

Spread
^^^^^^

StdDev
^^^^^^

Sum
^^^

Query selectors function
~~~~~~~~~~~~~~~~~~~~~~~~

Usage :

.. code:: python

    from influxable.db.function import selectors
    res = Query()\
        .select(selectors.Min('value'), selectors.Max('value'))\
        .from_measurements('param1')\
        .execute()

Bottom
^^^^^^

First
^^^^^

Last
^^^^

Max
^^^

Min
^^^

Percentile
^^^^^^^^^^

Sample
^^^^^^

Top
^^^

Query transformations function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage :

.. code:: python

    from influxable.db.function import selectors, transformations
    res = Query()\
        .select(transformations.Abs('value'))\
        .from_measurements('param1')\
        .execute()

.. code:: python

    from influxable.db.function.selectors import Min, Max
    from influxable.db.function.transformations import Abs
    res = Query()\
        .select(Abs(Min('value')), Abs(Max('value')))\
        .from_measurements('param1')\
        .execute()

Abs
^^^

ACos
^^^^

ASin
^^^^

ATan
^^^^

ATan2
^^^^^

Ceil
^^^^

Cos
^^^

CumulativeSum
^^^^^^^^^^^^^

Derivative
^^^^^^^^^^

Difference
^^^^^^^^^^

Elapsed
^^^^^^^

Exp
^^^

Floor
^^^^^

Histogram
^^^^^^^^^

Ln
^^

Log
^^^

Log2
^^^^

Log10
^^^^^

MovingAverage
^^^^^^^^^^^^^

NonNegativeDerivative
^^^^^^^^^^^^^^^^^^^^^

NonNegativeDifference
^^^^^^^^^^^^^^^^^^^^^

Pow
^^^

Round
^^^^^

Sin
^^^

Sqrt
^^^^

Tan
^^^

InfluxDBAdmin
~~~~~~~~~~~~~

alter\_retention\_policy()
^^^^^^^^^^^^^^^^^^^^^^^^^^

-  policy\_name

-  duration (default=None)

-  replication (default=None)

-  shard\_duration (default=None)

-  is\_default (default=False)

.. code:: sql

    ALTER RETENTION POLICY {policy_name} ON {database_name} [DURATION {duration} REPLICATION {replication} SHARD DURATION {shard_duration} DEFAULT]

create\_database()
^^^^^^^^^^^^^^^^^^

-  new\_database\_name

-  duration (default=None)

-  replication (default=None)

-  shard\_duration (default=None)

-  policy\_name (default=False)

.. code:: sql

    CREATE DATABASE {new_database_name} [WITH DURATION {duration} REPLICATION {replication} SHARD DURATION {shard_duration} NAME {policy_name}]

create\_retention\_policy()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  policy\_name

-  duration (default=None)

-  replication (default=None)

-  shard\_duration (default=None)

-  is\_default (default=False)

.. code:: sql

    CREATE RETENTION POLICY {policy_name} ON {database_name} [DURATION {duration} REPLICATION {replication} SHARD DURATION {shard_duration} DEFAULT]

create\_subscription()
^^^^^^^^^^^^^^^^^^^^^^

-  subscription\_name

-  hosts

-  any (default=False)

.. code:: sql

    CREATE SUBSCRIPTION {subscription_name} ON {database_name} DESTINATIONS ANY/ALL {hosts}

create\_user()
^^^^^^^^^^^^^^

-  user\_name

-  password

-  with\_privileges (default=False)

.. code:: sql

    CREATE USER {user_name} WITH PASSWORD {password} [WITH ALL PRIVILEGES]

delete()
^^^^^^^^

-  measurements (default=[])

-  criteria (default=[])

.. code:: sql

    DELETE FROM {measurements} WHERE {criteria}

drop\_continuous\_query()
^^^^^^^^^^^^^^^^^^^^^^^^^

-  query\_name

.. code:: sql

    DROP CONTINUOUS QUERY {query_name} ON {database_name}

drop\_database()
^^^^^^^^^^^^^^^^

-  database\_name\_to\_delete

.. code:: sql

    DROP DATABASE {database_name_to_delete}

drop\_measurement()
^^^^^^^^^^^^^^^^^^^

-  measurement\_name

.. code:: sql

    DROP MEASUREMENT {measurement_name}

drop\_retention\_policy()
^^^^^^^^^^^^^^^^^^^^^^^^^

-  policy\_name

.. code:: sql

    DROP RETENTION POLICY {policy_name} ON {database_name}

drop\_series()
^^^^^^^^^^^^^^

-  measurements (default=[])

-  criteria (default=[])

.. code:: sql

    DROP SERIES FROM {measurements} WHERE {criteria}

drop\_subscription()
^^^^^^^^^^^^^^^^^^^^

-  subscription\_name

.. code:: sql

    DROP SUBSCRIPTION {subscription_name} ON {full_database_name}

drop\_user()
^^^^^^^^^^^^

-  user\_name

.. code:: sql

    DROP USER {user_name}

explain()
^^^^^^^^^

-  query

-  analyze (default=False)

.. code:: sql

    EXPLAIN [ANALYZE] {query}

grant()
^^^^^^^

-  privilege

-  user\_name

.. code:: sql

    GRANT {privilege} ON {database_name} TO {user_name}

kill()
^^^^^^

-  query\_id

.. code:: sql

    KILL QUERY {query_id}

revoke()
^^^^^^^^

-  privilege

-  user\_name

.. code:: sql

    REVOKE {privilege} ON {database_name} FROM {user_name}

show\_field\_key\_cardinality()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  exact (default=False)

.. code:: sql

    SHOW FIELD KEY [EXACT] CARDINALITY

show\_measurement\_cardinality()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  exact (default=False)

.. code:: sql

    SHOW MEASUREMENT [EXACT] CARDINALITY

show\_series\_cardinality()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  exact (default=False)

.. code:: sql

    SHOW SERIES [EXACT] CARDINALITY

show\_tag\_key\_cardinality()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  key

-  exact (default=False)

.. code:: sql

    SHOW TAG VALUES [EXACT] CARDINALITY WITH KEY = {key}

show\_continuous\_queries()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: sql

    SHOW CONTINUOUS QUERIES

show\_diagnostics()
^^^^^^^^^^^^^^^^^^^

.. code:: sql

    SHOW DIAGNOSTICS

show\_field\_keys()
^^^^^^^^^^^^^^^^^^^

-  measurements (default=[])

.. code:: sql

    SHOW FIELD KEYS FROM {measurements}

show\_grants()
^^^^^^^^^^^^^^

-  user\_name

.. code:: sql

    SHOW GRANTS FOR {user_name}

show\_databases()
^^^^^^^^^^^^^^^^^

.. code:: sql

    SHOW DATABASES

show\_measurements()
^^^^^^^^^^^^^^^^^^^^

-  criteria (default=[])

.. code:: sql

    SHOW MEASUREMENTS WHERE {criteria}

show\_queries()
^^^^^^^^^^^^^^^

.. code:: sql

    SHOW QUERIES

show\_retention\_policies()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: sql

    SHOW RETENTION POLICIES

show\_series()
^^^^^^^^^^^^^^

-  measurements (default=[])

-  criteria (default=[])

-  limit (default=None)

-  offset (default=None)

.. code:: sql

    SHOW SERIES ON {database_name} [FROM {measurements} WHERE {criteria} LIMIT {limit} OFFSET {offset}]

show\_stats()
^^^^^^^^^^^^^

.. code:: sql

    SHOW STATS

show\_shards()
^^^^^^^^^^^^^^

.. code:: sql

    SHOW SHARDS

show\_shard\_groups()
^^^^^^^^^^^^^^^^^^^^^

.. code:: sql

    SHOW SHARD GROUPS

show\_subscriptions()
^^^^^^^^^^^^^^^^^^^^^

.. code:: sql

    SHOW SUBSCRIPTIONS

show\_tag\_keys()
^^^^^^^^^^^^^^^^^

-  measurements (default=[])

.. code:: sql

    SHOW TAG KEYS [FROM {measurements}]

show\_tag\_values()
^^^^^^^^^^^^^^^^^^^

-  key

-  measurements (default=[])

.. code:: sql

    SHOW TAG VALUES [FROM {measurements}] WITH KEY = {key}

show\_users()
^^^^^^^^^^^^^

.. code:: sql

    SHOW USERS

Exceptions
~~~~~~~~~~

InfluxDBException
^^^^^^^^^^^^^^^^^

InfluxDBError
^^^^^^^^^^^^^

InfluxDBConnectionError
^^^^^^^^^^^^^^^^^^^^^^^

InfluxDBInvalidResponseError
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

InfluxDBInvalidChoiceError
^^^^^^^^^^^^^^^^^^^^^^^^^^

InfluxDBInvalidTypeError
^^^^^^^^^^^^^^^^^^^^^^^^

InfluxDBInvalidURLError
^^^^^^^^^^^^^^^^^^^^^^^

InfluxDBBadRequestError
^^^^^^^^^^^^^^^^^^^^^^^

InfluxDBBadQueryError
^^^^^^^^^^^^^^^^^^^^^

InfluxDBInvalidNumberError
^^^^^^^^^^^^^^^^^^^^^^^^^^

InfluxDBInvalidTimestampError
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

InfluxDBUnauthorizedError
^^^^^^^^^^^^^^^^^^^^^^^^^

InfluxDBAttributeValueError
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Testing
-------

First, you need to install pytest via the file *requirements-test.txt*

.. code:: bash

    pip install -r requirements-test.txt

Then, you can launch the *pytest* command.

.. code:: python

    pytest -v

Supporting
----------

Feel free to post issues your feedback or if you reach a problem with influxable library.

If you want to contribute, please use the pull requests section.

Versioning
----------

We use `SemVer <http://semver.org/>`__ for versioning. For the versions available, see the `tags on this repository <https://github.com/Javidjms/influxable/releases>`__

Contributors
------------

-  `Javid Mougamadou <https://github.com/Javidjms>`__

Credits
-------

-  Logo designed by `Maxime Bergerard <https://github.com/maximebergerard>`__

References
----------

-  `Influxdb Website <https://docs.influxdata.com/platform/introduction>`__

-  `Influxdb Github Repository <https://github.com/influxdata/influxdb>`__

-  `Influxdb-Python Github Repository <https://github.com/influxdata/influxdb-python>`__

License
-------

`MIT <LICENSE.txt>`__

.. |pypi version| image:: https://img.shields.io/badge/pypi-1.3.0-blue
   :target: https://pypi.org/project/influxable/
.. |build status| image:: https://img.shields.io/badge/build-passing-green
.. |code coverage| image:: https://img.shields.io/badge/coverage-100-green
.. |license: MIT| image:: https://img.shields.io/badge/License-MIT-blue.svg
