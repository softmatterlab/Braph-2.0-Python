from abc import ABC, abstractmethod

class Subject:
    def __init__(self, id = 'sub_id'):
        self.id = id
        self.data_dict = {}

    @abstractmethod
    def init_data_dict(self):
        pass

    @abstractmethod
    def update_brain_atlases(self, atlases):
        pass
