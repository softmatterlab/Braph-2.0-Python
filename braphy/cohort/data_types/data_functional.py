from braphy.cohort.data_types.data import Data
import numpy as np

class DataFunctional(Data):
    def __init__(self, size = 0):
        super().__init__()
        self.value = np.zeros([1, size])

    def to_dict(self):
        d = {}
        d['value'] = self.value.tolist()
        return d

    def from_dict(self, d):
        self.set_value(np.asarray(d['value']))

    def add_row(self):
        new_row = np.zeros(np.size(self.value, 1))
        self.value = np.vstack([self.value, new_row])

    def remove_row(self):
        if np.size(self.value, 0) > 1:
            self.value = self.value[:-1, :]

    def get_subgraph_data(self, selected_nodes):
        new_value = self.value[:, selected_nodes]
        new_data = DataFunctional()
        new_data.set_value(new_value)
        return new_data