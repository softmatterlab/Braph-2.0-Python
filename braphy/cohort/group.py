import numpy as np
from braphy.cohort.subjects import *
import statistics

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

    def from_dict(d):
        subjects = []
        subject_class = eval(d['subject_class'])
        for subject_dict in d['subjects']:
            subjects.append(subject_class.from_dict(subject_dict))
        return Group(subject_class, subjects=subjects, name=d['name'], description=d['description'])

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
