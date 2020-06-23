from abc import ABC, abstractmethod
from braphy.utility.helper_functions import equal_around

class Data:
    def __init__(self):
        self.value = None

    def set_value(self, value):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return equal_around(self.value, other.value)

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def from_dict(self, d):
        pass

    def get_subgraph_data(self, selected_nodes):
        return self

