from abc import ABC, abstractmethod

class Subject:
    def __init__(self, atlases, id, groups):
        self.atlases = atlases
        self.id = id
        self.groups = groups

    @abstractmethod
    def initialize_datadict(self):
        pass

    @abstractmethod
    def update_brainatlases(self, atlases):
        pass
