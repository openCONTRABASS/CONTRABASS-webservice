from json import JSONEncoder

class WebsocketEvent:

    def __init__(self, event, message):
        self.event = event
        self.message = message

    @property
    def event_attr(self):
        return self.event

    @event_attr.setter
    def event_attr(self, event):
        self.event = event

    @property
    def message_attr(self):
        return self.message

    @message_attr.setter
    def message_attr(self, message):
        self.message = message

class ResponseWebsocketEventEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__