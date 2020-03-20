from abc import ABC, abstractmethod
from braphy.cohort.data_types.data import Data

class Subject:
    def __init__(self, id = 'sub_id'):
        self.id = id
        self.data_dict = {}
        self.init_data_dict()

    def to_dict(self):
        d = {}
        d['id'] = self.id
        d['data_dict'] = {}
        for key, value in self.data_dict.items():
            d['data_dict'][key] = value.to_dict()
        return d

    @classmethod
    def from_dict(cls, d):
        subject = cls(id = d['id'])
        for key, value in d['data_dict'].items():
            subject.data_dict[key].from_dict(value)
        return subject

    @abstractmethod
    def init_data_dict(self):
        self.data_dict['data'] = Data()

    @abstractmethod
    def from_txt(file_txt):
        pass
