from braphy.cohort.subjects.subject import Subject
from braphy.utility.helper_functions import abs_path_from_relative

class Cohort:
    def __init__(self, name, subject_class, subjects = None):
        self.name = name
        self.subject_class = subject_class
        self.groups = {}
        if subjects:
            self.subjects = subjects
        else:
            self.subjects = []

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
        if (len(selected) > 0) & (len(selected) < self.brain_region_number()):
            last_index_to_process = len(selected) - 1
            unprocessable_length = self.brain_region_number() - 1
            while (last_index_to_process >= 0) \
                  & (selected[last_index_to_process] == unprocessable_length):
                last_index_to_process = last_index_to_process - 1
                unprocessable_length = unprocessable_length - 1

            for i in range(last_index_to_process, -1, -1):
                self.invert_brain_regions(selected[i], selected[i] + 1)
                selected[i] = selected[i] + 1
        return selected

    def move_to_top_subjects(self, selected):
        if len(selected) > 0:
            for i in range(len(selected)):
                self.move_to_brain_region(selected[i], i)
            selected = np.arange(0, len(selected))
        return selected

    def move_to_bottom_subjects(self, selected):
        if len(selected) > 0:
            for i in range(len(selected) - 1, -1, -1):
                self.move_to_brain_region(selected[i], self.brain_region_number() - (len(selected) - i))
            selected = np.arange(self.brain_region_number() - len(selected), self.brain_region_number())
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
