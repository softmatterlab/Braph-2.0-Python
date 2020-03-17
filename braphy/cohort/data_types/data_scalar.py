from braphy.cohort.datas.data import Data

class DataScalar(Data):
    def __init__(self, value):
        super().__init__(value)