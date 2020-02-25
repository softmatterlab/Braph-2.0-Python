from abc import ABC, abstractmethod

class Measure(ABC):

    @abstractmethod
    def compute_measure():
        pass


    @abstractmethod
    def get_valid_graph_types():
        ''' Returns a dictionary where the keys are graph types and values are valid measures for 
        that type '''
        pass

    @abstractmethod
    def get_description():
        pass

    @abstractmethod
    def get_name():
        pass