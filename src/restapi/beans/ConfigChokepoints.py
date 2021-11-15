
class ConfigReactionsSets:

    def __init__(self):
        self.__objective = None
        self.__fraction_of_optimum = None

    @property
    def objective(self):
        return self.__objective

    @objective.setter
    def objective(self, objective):
        self.__objective = objective

    @property
    def fraction_of_optimum(self):
        return self.__fraction_of_optimum

    @fraction_of_optimum.setter
    def fraction_of_optimum(self, fraction_of_optimum):
        self.__fraction_of_optimum = fraction_of_optimum
