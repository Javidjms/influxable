import os

INFLUXDB_URL = os.getenv('INFLUXDB_URL', 'http://localhost:8086')
INFLUXDB_USER = os.getenv('INFLUXDB_USER', 'admin')
