import json
from braphy.cohort.subjects import *
from braphy.cohort.group import Group
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

    def invert_groups(self, i, j):
        tmp_group = self.groups[i]
        self.groups[i] = self.groups[j]
        self.groups[j] = tmp_group

    def move_up_groups(self, selected):
        if len(selected) > 0:
            first_index_to_process = 0
            unprocessable_length = 0
            while True:
                if (first_index_to_process >= len(self.groups)):
                    break
                if (first_index_to_process >= len(selected)):
                    break
                if (selected[first_index_to_process] != unprocessable_length):
                    break
                first_index_to_process = first_index_to_process + 1
                unprocessable_length = unprocessable_length + 1

            for i in range(first_index_to_process, len(selected)):
                self.invert_groups(selected[i], selected[i] - 1)
                selected[i] = selected[i] - 1
        return selected

    def move_down_groups(self, selected):
        if (len(selected) > 0) & (len(selected) < len(self.groups)):
            last_index_to_process = len(selected) - 1
            unprocessable_length = len(self.groups) - 1
            while (last_index_to_process >= 0) \
                  & (selected[last_index_to_process] == unprocessable_length):
                last_index_to_process = last_index_to_process - 1
                unprocessable_length = unprocessable_length - 1

            for i in range(last_index_to_process, -1, -1):
                self.invert_groups(selected[i], selected[i] + 1)
                selected[i] = selected[i] + 1
        return selected

    def add_subject(self, i = None, subject = None):
        if not i:
            i = len(self.subjects)
        if not subject:
            subject = self.subject_class(id = 'sub_{}'.format(len(self.subjects)))
        self.subjects.insert(i, subject)

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

    def invert_subjects(self, i, j):
        tmp_subject = self.subjects[i]
        self.subjects[i] = self.subjects[j]
        self.subjects[j] = tmp_subject

    def move_to_subject(self, i, j):
        if (i >= 0) & (i < len(self.subjects)) & (j >= 0) & (j < len(self.subjects)) & (i != j):
            subject = self.subjects[i]
            self.remove_subject(i)
            self.add_subject(j, subject)

    def add_above_subjects(self, selected):
        for i in range(len(selected) - 1, -1, -1):
            self.add_subject(i)
        selected = selected + np.array(range(1, len(selected) + 1))
        added = selected - 1
        return selected, added

    def add_below_subjects(self, selected):
        for i in range(len(selected) - 1, -1, -1):
            self.add_subject(i + 1)
        selected = selected + np.array(range(0, len(selected)))
        added = selected + 1
        return selected, added

    def move_up_subjects(self, selected):
        if len(selected) > 0:
            first_index_to_process = 0
            unprocessable_length = 0
            while True:
                if (first_index_to_process >= len(self.subjects)):
                    break
                if (first_index_to_process >= len(selected)):
                    break
                if (selected[first_index_to_process] != unprocessable_length):
                    break
                first_index_to_process = first_index_to_process + 1
                unprocessable_length = unprocessable_length + 1

            for i in range(first_index_to_process, len(selected)):
                self.invert_subjects(selected[i], selected[i] - 1)
                selected[i] = selected[i] - 1
        return selected

    def move_down_subjects(self, selected):
        if (len(selected) > 0) & (len(selected) < len(self.subjects)):
            last_index_to_process = len(selected) - 1
            unprocessable_length = len(self.subjects) - 1
            while (last_index_to_process >= 0) \
                  & (selected[last_index_to_process] == unprocessable_length):
                last_index_to_process = last_index_to_process - 1
                unprocessable_length = unprocessable_length - 1

            for i in range(last_index_to_process, -1, -1):
                self.invert_subjects(selected[i], selected[i] + 1)
                selected[i] = selected[i] + 1
        return selected

    def move_to_top_subjects(self, selected):
        if len(selected) > 0:
            for i in range(len(selected)):
                self.move_to_subject(selected[i], i)
            selected = np.arange(0, len(selected))
        return selected

    def move_to_bottom_subjects(self, selected):
        if len(selected) > 0:
            for i in range(len(selected) - 1, -1, -1):
                self.move_to_subject(selected[i], len(self.subjects) - (len(selected) - i))
            selected = np.arange(len(self.subjects) - len(selected), len(self.subjects))
        return selected

    def invert_group(self, group_idx):
        group = self.groups[group_idx]
        subjects = [subject for subject in self.subjects if subject not in group.subjects]
        group.subjects = subjects

    def merge_groups(self, group_idx1, group_idx2):
        if group_idx1 == group_idx2:
            return
        group1 = self.groups[group_idx1]
        group2 = self.groups[group_idx2]
        subjects = [subject for subject in group1.subjects]
        subjects.extend([subject for subject in group2.subjects if subject not in subjects])
        group = Group(self.subject_class, name = self.new_group_name(), subjects = subjects)
        self.add_group(group = group)

    def intersect_groups(self, group_idx1, group_idx2):
        if group_idx1 == group_idx2:
            return
        group1 = self.groups[group_idx1]
        group2 = self.groups[group_idx2]
        subjects = [subject for subject in group1.subjects if subject in group2.subjects]
        group = Group(self.subject_class, name = self.new_group_name(), subjects = subjects)
        self.add_group(group = group)

    def load_from_file(self, file_name, subject_load_function):
        group_name = file_name.split('/')[-1]
        group = Group(self.subject_class, name = group_name)
        subjects = subject_load_function(file_name)
        group.add_subjects(subjects)
        self.add_group(group=group)
        self.subjects.extend(subjects)

    def load_from_txt(self, file_name):
        self.load_from_file(file_name, self.subject_class.from_txt)

    def load_from_xml(self, file_name):
        self.load_from_file(file_name, self.subject_class.from_xml)

    def load_from_xlsx(self, file_name):
        self.load_from_file(file_name, self.subject_class.from_xlsx)
