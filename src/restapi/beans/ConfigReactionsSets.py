from .OptimizationEnum import *
from .MediumEnum import *

class ConfigReactionsSets:

    def __init__(self):
        self.__objective = None
        self.__fraction_of_optimum = None
        self.__optimization = OptimizationEnum.FBA
        self.__medium = MediumEnum.DEFAULT
        self.__skip_knockout_computation = True

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

    @property
    def optimization(self):
        return self.__optimization

    @optimization.setter
    def optimization(self, optimization):
        self.__optimization = optimization

    @property
    def medium(self):
        return self.__medium

    @medium.setter
    def medium(self, medium):
        self.__medium = medium

    @property
    def skip_knockout_computation(self):
        return self.__skip_knockout_computation

    @skip_knockout_computation.setter
    def skip_knockout_computation(self, skip_knockout_computation):
        self.__skip_knockout_computation = skip_knockout_computation
