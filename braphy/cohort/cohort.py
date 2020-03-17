from braphy.cohort.subjects.subject import Subject
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.cohort.group import Group

class Cohort:
    def __init__(self, name, subject_class, subjects = None):
        self.name = name
        self.subject_class = subject_class
        self.groups = []
        if subjects:
            self.subjects = subjects
        else:
            self.subjects = []

    def add_group(self, group = None):
        if not group:
            group = Group(self.subject_class)
        self.groups.append(group)

    def remove_group(self, i):
        self.groups.remove(i)

    def remove_groups(self, selected):
        for i in selected:
            self.remove_group(i)

    def invert_groups(self, i, j):
        tmp_group = self.groups[i]
        self.groups[i] = self.groups[j]
        self.groups[j] = tmp_group

    def move_up_group(self, selected):
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

    def add_subject(self, i, subject = None):
        if not subject:
            subject = Subject()
        self.subjects.insert(i, subject)

    def remove_subject(self, i):
        self.subjects.remove(i)

    def replace_subject(self, i, subject):
        self.subjects[i] = subject

    def invert_subjects(self, i, j):
        tmp_subject = self.subjects[i]
        self.subjects[i] = self.subjects[j]
        self.subjects[j] = tmp_subject

    def move_to_subject(self, i, j):
        subject = self.subjects[i]
        self.remove_subject(i)
        self.add_subject(subject, j)

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

    def add_subject_to_group(self, subject, group_name):
        if group_name not in self.groups.keys():
            self.groups[group_name] = {'description': '',
                                       'subjects': []}
        self.groups[group_name]['subjects'].append(subject)

    def add_subjects_to_group(self, subjects, group_name):
        if group_name not in self.groups.keys():
            self.groups[group_name] = {'description': '',
                                       'subjects': []}
        self.groups[group_name]['subjects'].extend(subjects)

    def remove_subjects_from_group(self, indices, group_name):
        for i in indices:
            self.groups[group_name]['subjects'].remove(i)

    def load_from_txt(self, file_path = '', file_name = ''):
        file_txt = abs_path_from_relative(__file__, file_path + file_name)
        self.subjects = self.subject_class.from_txt(file_txt)
