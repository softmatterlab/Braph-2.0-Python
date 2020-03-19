from abc import ABC, abstractmethod
from braphy.cohort.data_types.data import Data

class Subject:
    def __init__(self, id = 'sub_id'):
        self.id = id
        self.data_dict = {}
        self.init_data_dict()

    @abstractmethod
    def init_data_dict(self):
        self.data_dict['data'] = Data()

    @abstractmethod
    def from_txt(file_txt):
        pass
