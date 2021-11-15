from json import JSONEncoder


class ResponseChannel:

    def __init__(self, channel=None):
        self.channel = channel

    @property
    def channel_attr(self):
        return self.channel

    @channel_attr.setter
    def channel_attr(self, channel):
        self.channel = channel

class ResponseChannelEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__