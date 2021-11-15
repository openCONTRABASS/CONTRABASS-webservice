

class Chokepoint:

    def __init__(self, reaction, metabolite):
        self.__reaction = reaction
        self.__metabolite = metabolite

    @property
    def reaction(self):
        return self.__reaction

    @reaction.setter
    def reaction(self, reaction):
        self.__reaction = reaction

    @property
    def metabolite(self):
        return self.__metabolite

    @metabolite.setter
    def metabolite(self, metabolite):
        self.__metabolite = metabolite
