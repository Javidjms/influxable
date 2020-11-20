class InfluxDBApi:
    @staticmethod
    def get_debug_requests(request, seconds=10):
        url = '/debug/requests'
        seconds = seconds if isinstance(seconds, int) else 10
        params = {'seconds': seconds}
        res = request.get(url=url, params=params)
        return res.json()

    @staticmethod
    def get_debug_vars(request):
        url = '/debug/vars'
        res = request.get(url=url)
        return res.json()

    @staticmethod
    def ping(request, verbose=False):
        url = '/ping'
        verbose = verbose if isinstance(verbose, bool) else False
        params = {'verbose': verbose} if verbose else {}
        res = request.get(url=url, params=params)
        return res.text or True

    @staticmethod
    def execute_query(
        request,
        query,
        method='get',
        chunked=False,
        epoch='ns',
        pretty=False,
    ):
        url = '/query'
        params = {
            'db': request.database_name,
            'q': query,
            'epoch': epoch,
            'chunked': chunked,
            'pretty': pretty,
        }
        res = request.request(method, url, params=params)
        return res.json()

    @staticmethod
    def write_points(
        request,
        points,
        precision='ns',
        consistency='all',
        retention_policy_name='DEFAULT',
    ):
        url = '/write'
        params = {
            'db': request.database_name,
            'precision': precision,
            'consistency': consistency,
            'retention_policy_name': retention_policy_name,
        }
        str_encoded_points = points.encode('utf-8')
        request.post(url, params=params, data=str_encoded_points)
        return True
