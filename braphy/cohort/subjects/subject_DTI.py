from braphy.cohort.subjects.subject import Subject
from braphy.cohort.data_types.data_scalar import DataScalar
from braphy.cohort.data_types.data_connectivity import DataConnectivity

class SubjectDTI(Subject):
    def __init__(self, id = 'sub_id'):
        super().__init__(id = id)

    def init_data_dict(self):
        self.data_dict['age'] = DataScalar()
        self.data_dict['DTI'] = DataConnectivity()
