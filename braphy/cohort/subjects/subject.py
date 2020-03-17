from abc import ABC, abstractmethod

class Subject:
    def __init__(self, id = 'sub_id'):
        self.id = id
        self.data_dict = {}
        self.init_data_dict()

    @abstractmethod
    def init_data_dict(self):
        pass

    @abstractmethod
    def from_txt(file_txt):
        pass
