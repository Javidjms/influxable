class InfluxDBException(Exception):
    pass


class InfluxDBError(InfluxDBException):
    pass


class InfluxDBConnectionError(InfluxDBError):
    pass


class InfluxDBInvalidResponseError(InfluxDBError):
    pass


class InfluxDBInvalidChoiceError(InfluxDBError):
    pass


class InfluxDBInvalidTypeError(InfluxDBError):
    pass


class InfluxDBInvalidURLError(InfluxDBError):
    MESSAGE_PLACEHOLDER = 'Bad schema for : {base_url}'

    def __init__(self, base_url):
        self.message = self.MESSAGE_PLACEHOLDER.format(base_url=base_url)
        super().__init__(self.message)


class InfluxDBBadRequestError(InfluxDBError):
    MESSAGE_PLACEHOLDER = 'Bad request for params : {params}'

    def __init__(self, params):
        self.message = self.MESSAGE_PLACEHOLDER.format(params=params)
        super().__init__(self.message)


class InfluxDBEmptyRequestError(InfluxDBError):
    MESSAGE_PLACEHOLDER = 'Empty request'

    def __init__(self, params):
        self.message = self.MESSAGE_PLACEHOLDER
        super().__init__(self.message)


class InfluxDBBadQueryError(InfluxDBError):
    MESSAGE_PLACEHOLDER = 'Invalid query : {query} - {error}'

    def __init__(self, query, error):
        self.message = self.MESSAGE_PLACEHOLDER.format(
            query=query,
            error=error,
        )
        super().__init__(self.message)


class InfluxDBInvalidNumberError(InfluxDBError):
    MESSAGE_PLACEHOLDER = 'Invalid number : {points}'

    def __init__(self, points):
        self.message = self.MESSAGE_PLACEHOLDER.format(points=points)
        super().__init__(self.message)


class InfluxDBInvalidTimestampError(InfluxDBError):
    MESSAGE_PLACEHOLDER = 'Invalid timestamp : {points}'

    def __init__(self, points):
        self.message = self.MESSAGE_PLACEHOLDER.format(points=points)
        super().__init__(self.message)


class InfluxDBUnauthorizedError(InfluxDBError):
    MESSAGE = 'Authorization Failed (Bad credentials)'

    def __init__(self, message):
        self.message = self.MESSAGE
        super().__init__(self.MESSAGE)


class InfluxDBAttributeValueError(InfluxDBError):
    pass
