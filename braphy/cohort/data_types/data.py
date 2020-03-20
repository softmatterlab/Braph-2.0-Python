from abc import ABC, abstractmethod

class Data:
    def __init__(self):
        self.value = None

    def set_value(self, value):
        self.value = value

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def from_dict(self, d):
        pass


