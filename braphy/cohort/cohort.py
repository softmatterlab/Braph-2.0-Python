import json
from braphy.cohort.subjects import *
from braphy.cohort.group import Group
from braphy.utility.helper_functions import ListManager as lm
import numpy as np

class Cohort:
    def __init__(self, name, subject_class, subjects = None, groups = None):
        self.name = name
        self.subject_class = subject_class
        if subjects:
            self.subjects = subjects
        else:
            self.subjects = []
        if groups:
            self.groups = groups
        else:
            self.groups = []

    def to_dict(self):
        d = {}
        d['name'] = self.name
        d['subject_class'] = self.subject_class.__name__
        subjects = []
        for subject in self.subjects:
            subjects.append(subject.to_dict())
        d['subjects'] = subjects
        groups = []
        for group in self.groups:
            groups.append(group.to_dict())
        d['groups'] = groups
        return d

    def from_dict(d):
        subjects = []
        subject_class = eval(d['subject_class'])
        for subject_dict in d['subjects']:
            subjects.append(subject_class.from_dict(subject_dict))
        groups = []
        for group_dict in d['groups']:
            groups.append(Group.from_dict(group_dict))
        return Cohort(d['name'], subject_class, subjects = subjects, groups = groups)

    def to_file(self, cohort_file):
        with open(cohort_file, 'w') as f:
            json.dump(self.to_dict(), f, sort_keys=True, indent=4)

    def from_file(cohort_file):
        with open(cohort_file, 'r') as f:
            d = json.load(f)
        return Cohort.from_dict(d)

    def group_averages(self):
        averages = []
        for group in self.groups:
            averages.append(group.averages())
        return np.array(averages)

    def group_standard_deviations(self):
        standard_deviations = []
        for group in self.groups:
            standard_deviations.append(group.standard_deviations())
        return np.array(standard_deviations)

    def new_group_name(self):
        return "Group_{}".format(len(self.groups))

    def add_group(self, group = None):
        if not group:
            group = Group(self.subject_class, name = self.new_group_name())
        self.groups.append(group)

    def remove_group(self, i):
        self.groups.remove(i)

    def remove_groups(self, selected):
        new_selected = list(selected)
        for i in range(len(selected) - 1, -1, -1):
            del self.groups[selected[i]]
            del new_selected[i]
        return np.array(new_selected)

    def remove_subjects_from_all_groups(self, selected):
        for i in range(len(selected)):
            subject = self.subjects[selected[i]]
            for j in range(len(self.groups)):
                group = self.groups[j]
                if subject in group.subjects:
                    group.remove_subject(subject)

    def swap_groups(self, i, j):
        lm.swap(self.groups, i, j)

    def move_up_groups(self, selected):
        return lm.move_up(self.groups, selected)

    def move_down_groups(self, selected):
        return lm.move_down(self.groups, selected)

    def new_group_from_selected(self, subject_indices):
        self.add_group()
        for index in subject_indices:
            self.groups[-1].add_subject(self.subjects[index])

    def new_subject(self):
        return self.subject_class(id = 'sub_{}'.format(len(self.subjects)))

    def add_subjects(self, subjects):
        added_subjects = []
        for subject in subjects:
            added_subjects.append(self.add_subject(subject = subject))
        return added_subjects

    def add_subject(self, i = None, subject = None):
        if not i:
            i = len(self.subjects)
        if not subject:
            subject = self.subject_class(id = 'sub_{}'.format(len(self.subjects)))
        for existing_subject in self.subjects:
            if subject == existing_subject:
                return existing_subject
        self.subjects.insert(i, subject)
        return subject

    def remove_subject(self, i):
        del self.subjects[i]

    def remove_subjects(self, selected):
        new_selected = list(selected)
        for i in range(len(selected) - 1, -1, -1):
            del self.subjects[selected[i]]
            del new_selected[i]
        return np.array(new_selected)

    def replace_subject(self, i, subject):
        self.subjects[i] = subject

    def swap_subjects(self, i, j):
        lm.swap(self.subjects, i, j)

    def move_to_subject(self, i, j):
        lm.move_to(self.subjects, i, j)

    def add_above_subjects(self, selected):
        return lm.add_above(self.subjects, selected, self.new_subject)

    def add_below_subjects(self, selected):
        return lm.add_below(self.subjects, selected, self.new_subject)

    def move_up_subjects(self, selected):
        return lm.move_up(self.subjects, selected)

    def move_down_subjects(self, selected):
        return lm.move_down(self.subjects, selected)

    def move_to_top_subjects(self, selected):
        return lm.move_to_top(self.subjects, selected)

    def move_to_bottom_subjects(self, selected):
        return lm.move_to_bottom(self.subjects, selected)

    def invert_groups(self, group_indices):
        group_subjects = []
        for group_idx in group_indices:
            group = self.groups[group_idx]
            group_subjects.extend([subject for subject in group.subjects])
        subjects = [subject for subject in self.subjects if subject not in group_subjects]
        group = Group(self.subject_class, name = self.new_group_name(), subjects = subjects)
        self.add_group(group = group)

    def merge_groups(self, group_indices):
        if len(group_indices) < 2:
            return
        subjects = []
        for group_idx in group_indices:
            group = self.groups[group_idx]
            subjects.extend([subject for subject in group.subjects if subject not in subjects])
        group = Group(self.subject_class, name = self.new_group_name(), subjects = subjects)
        self.add_group(group = group)

    def intersect_groups(self, group_indices):
        if len(group_indices) < 2:
            return
        group = self.groups[group_indices[0]]
        subjects = set(group.subjects)
        for i in range(1, len(group_indices)):
            group_idx = group_indices[i]
            group = self.groups[group_idx]
            subjects = subjects.intersection(set(group.subjects))
        subjects = list(subjects)
        group = Group(self.subject_class, name = self.new_group_name(), subjects = subjects)
        self.add_group(group = group)

    def load_from_file(self, file_name, subject_load_function):
        group_name = file_name.split('/')[-1]
        group = Group(self.subject_class, name = group_name)
        subjects = subject_load_function(file_name)
        subjects = self.add_subjects(subjects)
        group.add_subjects(subjects)
        self.add_group(group=group)

    def save_to_txt(self, file_name):
        s = " "
        for subject in self.subjects:
            s += "\n{}".format(str(subject))
        with open(file_name, 'w') as f:
            f.write(s)

    def load_from_txt(self, file_name):
        self.load_from_file(file_name, self.subject_class.from_txt)

    def load_from_xml(self, file_name):
        self.load_from_file(file_name, self.subject_class.from_xml)

    def load_from_xlsx(self, file_name):
        self.load_from_file(file_name, self.subject_class.from_xlsx)
