from braphy.cohort.data_types.data import Data
import numpy as np

class DataStructural(Data):
    def __init__(self, size = 0):
        super().__init__()
        self.value = np.zeros(size)

    def to_dict(self):
        d = {}
        d['value'] = self.value.tolist()
        return d

    def from_dict(self, d):
        self.set_value(np.asarray(d['value']))

    def get_subgraph_data(self, selected_nodes):
        new_value = self.value[selected_nodes]
        new_data = DataStructural()
        new_data.set_value(new_value)
        return new_data
