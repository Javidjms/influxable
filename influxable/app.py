from .helpers.decorators import Singleton
from .connection import Connection


@Singleton
class Influxable:
    def __init__(self):
        self.connection = Connection()
    
