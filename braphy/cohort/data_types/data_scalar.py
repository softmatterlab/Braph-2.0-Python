from braphy.cohort.data_types.data import Data

class DataScalar(Data):
    def __init__(self, value):
        super().__init__(value)