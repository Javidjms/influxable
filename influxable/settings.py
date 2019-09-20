import os

INFLUXDB_URL = os.getenv('INFLUXDB_URL', 'http://localhost:8086')
INFLUXDB_USER = os.getenv('INFLUXDB_USER', 'admin')
INFLUXDB_PASSWORD = os.getenv('INFLUXDB_PASSWORD', 'changeme')
INFLUXDB_DATABASE_NAME = os.getenv('INFLUXDB_DATABASE_NAME', 'default')
