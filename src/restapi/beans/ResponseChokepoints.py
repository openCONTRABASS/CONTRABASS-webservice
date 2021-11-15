from json import JSONEncoder


class ResponseChokepoints:

    def __init__(self, status=None, finished=None, result=None, pending_length=None):
        self.__status = status
        self.__finished = finished
        self.__result = result
        self.__pending_length = pending_length

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def finished(self):
        return self.__finished

    @finished.setter
    def finished(self, finished):
        self.__finished = finished

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, result):
        self.__result = result

    @property
    def pending_length(self):
        return self.__pending_length

    @pending_length.setter
    def pending_length(self, pending_length):
        self.__pending_length = pending_length

class ResponseChokepointsEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__