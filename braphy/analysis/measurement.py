from braphy.workflows.MRI.subject_MRI import SubjectMRI
from braphy.workflows.fMRI.subject_fMRI import SubjectfMRI

class Measurement():
    def __init__(self, group, measure_class, sub_measure, value = None):
        self.group = group
        self.measure_class = measure_class
        self.sub_measure = sub_measure
        self.value = value

    def to_dict(self):
        d = {}
        d['groups'] = [str(group) for group in self.groups]
        d['measure_class'] = self.measure_class.__name__
        d['sub_measure'] = self.sub_measure
        return d

    def from_dict(d):
        groups = [int(group) for group in d['groups']]
        measure_class = eval(d['measure_class'])
        sub_measure = d['sub_measure']
        return Measurement(groups, measure_class, sub_measure)

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
