from json import JSONEncoder


class ResponseEndpoint:

    def __init__(self, endpoint=None):
        self.endpoint = endpoint

    @property
    def endpoint_attr(self):
        return self.endpoint

    @endpoint_attr.setter
    def endpoint_attr(self, endpoint):
        self.endpoint = endpoint

class ResponseEndpointEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__