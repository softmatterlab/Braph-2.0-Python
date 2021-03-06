from abc import ABC, abstractmethod
from braphy.cohort.data_types.data import Data

class Subject:
    def __init__(self, id = 'sub_id', size = 0):
        self.id = id
        self.data_dict = {}
        self.init_data_dict(size)

    def equals(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.id != other.id:
            return False
        for key, value in self.data_dict.items():
            if value != other.data_dict[key]:
                return False
        return True

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

    @classmethod
    def data_type(cls):
        return cls.__name__.split('Subject')[1]

    @abstractmethod
    def to_txt(subjects, file_name, labels):
        pass

    @abstractmethod
    def to_xlsx(subjects, file_name, labels):
        pass

    @abstractmethod
    def init_data_dict(self):
        self.data_dict['data'] = Data()

    @abstractmethod
    def from_txt(file_txt):
        pass

    @abstractmethod
    def correlation(subjects):
        pass

    @abstractmethod
    def structural():
        pass

    @abstractmethod
    def functional():
        pass

    def get_subgraph_subject(self, selected_nodes):
        new_data_dict = {}
        for key, data in self.data_dict.items():
            new_data_dict[key] = data.get_subgraph_data(selected_nodes)
        new_subject = self.__class__(self.id)
        new_subject.data_dict = new_data_dict
        return new_subject
