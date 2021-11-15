

class Model:

    def __init__(self, uuid=None, url=None):
        self.__uuid = uuid
        self.__url = url

    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, uuid):
        self.__uuid = uuid

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

