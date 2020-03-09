from abc import ABC, abstractmethod
import re

class Measure(ABC):

    @abstractmethod
    def compute_measure():
        pass


    @abstractmethod
    def get_valid_graph_types():
        ''' Returns a dictionary where the keys are graph types and values \
            are valid measures for that type '''
        pass

    @abstractmethod
    def get_description():
        pass

    @abstractmethod
    def get_name():
        pass
    
    def community_dependent():
        return False

    @classmethod
    def get_name(cls):
        split_name = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', cls.__name__)).split()
        if(len(split_name)<=1):
            return ""
        name = split_name[1]
        for word in split_name[2:]:
            name = "{} {}".format(name, word.lower())
        return name

