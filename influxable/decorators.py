import requests
from . import exceptions


def raise_if_error(func):
    def func_wrapper(*args, **kwargs):
        try:
            params = kwargs.get('params', {})
            res = func(*args, **kwargs)
            res.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            raise exceptions.InfluxDBConnectionError(err)
        except requests.exceptions.HTTPError as err:
            if res.status_code == 400:
                raise exceptions.InfluxDBBadRequestError(params)
            raise err
        return res
    return func_wrapper