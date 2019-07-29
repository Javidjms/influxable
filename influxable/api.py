import json


class InfluxDBApi:
    @staticmethod
    def get_debug_requests(request, seconds=10):
        url = '/debug/requests'
        params = {'seconds': seconds}
        res = request.get(url=url, params=json.dumps(params))
        return res.json()

    @staticmethod
    def get_debug_vars(request):
        url = '/debug/vars'
        res = request.get(url=url)
        return res.json()
