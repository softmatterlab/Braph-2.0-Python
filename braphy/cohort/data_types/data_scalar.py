from braphy.cohort.data_types.data import Data

class DataScalar(Data):
    def __init__(self):
        super().__init__()
        self.value = 0

    def to_dict(self):
        d = {}
        d['value'] = self.value
        return d

    def from_dict(self, d):
        self.set_value(d['value'])
