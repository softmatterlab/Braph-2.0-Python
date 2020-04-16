from braphy.cohort.data_types.data import Data
import numpy as np

class DataFunctional(Data):
    def __init__(self, size = 0):
        super().__init__()
        self.value = np.zeros([size, 0])

    def to_dict(self):
        d = {}
        d['value'] = self.value.tolist()
        return d

    def from_dict(self, d):
        self.set_value(np.asarray(d['value']))
