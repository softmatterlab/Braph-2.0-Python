from braphy.cohort.data_types.data import Data

class DataScalar(Data):
    def __init__(self):
        super().__init__()

    def to_dict(self):
        d = {}
        d['value'] = self.value
        return d

    def from_dict(self, d):
        self.set_value(d['value'])
