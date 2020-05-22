import numpy as np
from braphy.utility.stat_functions import StatFunctions as stat
from braphy.utility.permutation import Permutation
import statistics
from braphy.workflows import *

class Group:
    def __init__(self, subject_class, subjects = None, name = 'Group', description = '-'):
        self.name = name
        self.subject_class = subject_class
        self.description = description
        if not subjects:
            subjects = []
        self.subjects = subjects

    def to_dict(self):
        d = {}
        d['name'] = self.name
        d['subject_class'] = self.subject_class.__name__
        d['description'] = self.description
        d['subjects'] = []
        for subject in self.subjects:
            d['subjects'].append(subject.to_dict())
        return d

    def from_dict(d, subjects):
        subject_class = eval(d['subject_class'])
        subjects_in_group = []
        for subject in subjects:
            for group_subject in [subject_class.from_dict(sub) for sub in d['subjects']]:
                if subject.equals(group_subject):
                    subjects_in_group.append(subject)
        return Group(subject_class, subjects=subjects_in_group, name=d['name'], description=d['description'])

    def add_subject(self, subject):
        self.subjects.append(subject)

    def add_subjects(self, subjects):
        self.subjects.extend(subjects)

    def remove_subject(self, subjects):
        self.subjects.remove(subjects)

    def remove_subjects(self, subjects):
        for subject in subjects:
            self.subjects.remove(subject)

    def averages(self):
        values = []
        for subject in self.subjects:
            values.append(subject.data_dict['data'].value)
        values = np.array(values)
        if values.size == 0:
            return []
        return values.mean(0)

    def standard_deviations(self):
        values = []
        for subject in self.subjects:
            values.append(subject.data_dict['data'].value)
        values = np.array(values)
        if values.size == 0:
            return []
        return values.std(0)

    def data_comparison(self, other, permutations = 1000):
        assert isinstance(other, Group), "{} is not a group".format(other.__class__.__name__)
        assert self.subject_class == other.subject_class, "{} and {} are different subject classes".format(self.subject_class.__name__, other.subject_class.__name__)
        assert len(self.subjects) > 0, "{} has no subjects".format(self.name)
        assert len(other.subjects) > 0, "{} has no subjects".format(other.name)

        values_self = np.array([subject.data_dict['data'].value for subject in self.subjects])
        values_other = np.array([subject.data_dict['data'].value for subject in other.subjects])

        subject_length_self = np.shape(values_self)[0]
        data_length_self = np.shape(values_self)[1]
        data_length_other = np.shape(values_other)[1]
        assert data_length_self == data_length_other, "Subject data length does not match: {} and {}".format(data_length_self, data_length_other)

        std_self = values_self.std(0)
        std_other = values_other.std(0)
        mean_self = values_self.mean(0)
        mean_other = values_other.mean(0)

        values_all = np.concatenate((values_self, values_other))

        diffs = []
        for _ in range(permutations):
            p1, p2 = Permutation.permute(values_self, values_other, False)
            diffs.append(p1.mean(0) - p2.mean(0))
        diffs = np.array(diffs)
        p_value_single = stat.p_value_one_tail(mean_self, diffs)
        p_value_double = stat.p_value_two_tail(mean_self, diffs)

        averages = [mean_self, mean_other]
        stds = [std_self, std_other]
        p_values = [p_value_single, p_value_double]

        return averages, stds, p_values

    def correlation(self):
        return self.subject_class.correlation(self.subjects)
