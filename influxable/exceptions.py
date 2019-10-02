class InfluxDBException(Exception):
    pass


class InfluxDBConnectionError(InfluxDBException):
    pass


class InfluxDBBadRequestError(InfluxDBException):
    MESSAGE_PLACEHOLDER = 'Bad request for params : {params}'

    def __init__(self, params):
        self.message = self.MESSAGE_PLACEHOLDER.format(params=params)
        super().__init__(self.message)


