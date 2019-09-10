import json
class DefaultSerializer:
    def __init__(self, response):
        self.response = response

    def convert(self):
        return self.response


class JsonSerializer(DefaultSerializer):
    def convert(self):
        return json.dumps(self.response.raw)


    pass

    pass
