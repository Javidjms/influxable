class DefaultSerializer:
    def __init__(self, response):
        self.response = response

    def convert(self):
        return self.response


class JsonSerializer(DefaultSerializer):
    pass

    pass
