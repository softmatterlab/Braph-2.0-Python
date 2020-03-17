from braphy.cohort.subjects.subject import Subject
from braphy.cohort.data_types.data_scalar import DataScalar
from braphy.cohort.data_types.data_structural import DataStructural

class SubjectMRI(Subject):
    def __init__(self, id = 'sub_id'):
        pass

    def init_data_dict(self):
        self.data_dict['age'] = DataScalar()
        self.data_dict['MRI'] = DataStructural()
