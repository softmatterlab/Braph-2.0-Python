from braphy.workflows.MRI.subject_MRI import SubjectMRI
from braphy.workflows.fMRI.subject_fMRI import SubjectfMRI
from braphy.graph.measures import *

class Measurement():
    def __init__(self, group, measure_class, sub_measure, value = None):
        self.group = group
        self.measure_class = measure_class
        self.sub_measure = sub_measure
        self.value = value

    def to_dict(self):
        d = {}
        d['group'] = str(self.group)
        d['measure_class'] = self.measure_class.__name__
        d['sub_measure'] = self.sub_measure
        d['value'] = self.value.tolist() if isinstance(self.value, np.ndarray) else self.value
        return d

    @classmethod
    def from_dict(cls, d):
        group = int(d['group'])
        measure_class = eval(d['measure_class'])
        sub_measure = d['sub_measure']
        value = d['value']
        value = np.array(value) if isinstance(value, list) else value
        return cls(group, measure_class, sub_measure, value)

    def get_value(self):
        return self.value

    def is_global(self):
        return self.measure_class.is_global(self.sub_measure)

    def is_nodal(self):
        return self.measure_class.is_nodal(self.sub_measure)

    def is_binodal(self):
        return self.measure_class.is_binodal(self.sub_measure)

    def dimension(self):
        return self.measure_class.dimension(self.sub_measure)
