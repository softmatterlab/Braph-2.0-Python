from braphy.cohort.data_types.data import Data
import numpy as np

class DataConnectivity(Data):
    def __init__(self):
        super().__init__()

    def to_dict(self):
        d = {}
        d['value'] = self.value.tolist()
        return d

    def from_dict(self, d):
        self.set_value(np.asarray(d['value']))
