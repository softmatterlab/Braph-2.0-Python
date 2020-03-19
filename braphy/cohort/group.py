import numpy as np

class Group:
    def __init__(self, subject_class, subjects = None, name = 'Group', description = '-'):
        self.name = name
        self.description = description
        self.subject_class = subject_class
        if not subjects:
            subjects = []
        self.subjects = subjects

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
