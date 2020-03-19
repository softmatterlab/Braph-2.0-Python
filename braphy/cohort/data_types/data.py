from abc import ABC, abstractmethod

class Data:
    def __init__(self):
        self.value = None

    def set_value(self, value):
        self.value = value
