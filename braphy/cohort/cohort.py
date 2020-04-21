import json
from braphy.cohort.subjects import *
from braphy.cohort.group import Group
from braphy.atlas.brain_atlas import BrainAtlas
from braphy.utility.helper_functions import ListManager as lm
import numpy as np

class Cohort:
    def __init__(self, name, subject_class, atlas, subjects = None, groups = None):
        self.name = name
        self.subject_class = subject_class
        self.atlas = atlas
        self.subjects = subjects if subjects else []
        self.groups = groups if groups else []
        self.new_groups_added = len(self.groups)
        self.new_subjects_added = len(self.subjects)

    def to_file(self):
        d = {}
        d['cohort'] = self.to_dict()
        with open(atlas_file, 'w') as f:
            json.dump(d, f, sort_keys=True, indent=4)

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
        d['atlas'] = self.atlas.to_dict()
        return d

    def from_file(cohort_file):
        with open(cohort_file, 'r') as f:
            d = json.load(f)
        return Cohort.from_dict(d['cohort'])

    def from_dict(d):
        subjects = []
        subject_class = eval(d['subject_class'])
        for subject_dict in d['subjects']:
            subjects.append(subject_class.from_dict(subject_dict))
        groups = []
        for group_dict in d['groups']:
            groups.append(Group.from_dict(group_dict))
        return Cohort(d['name'], subject_class, BrainAtlas.from_dict(d['atlas']), subjects = subjects, groups = groups)

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
        unique = False
        while not unique:
            self.new_groups_added += 1
            name = "Group_{}".format(self.new_groups_added)
            unique = True
            for group in self.groups:
                if group.name == name:
                    unique = False
        return "Group_{}".format(self.new_groups_added)

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

    def new_subject_id(self):
        unique = False
        while not unique:
            self.new_subjects_added += 1
            id = "sub_{}".format(self.new_subjects_added)
            unique = True
            for subject in self.subjects:
                if subject.id == id:
                    unique = False
        return 'sub_{}'.format(self.new_subjects_added)

    def new_subject(self):
        return self.subject_class(id = self.new_subject_id(), size = self.atlas.brain_region_number())

    def add_subjects(self, subjects):
        added_subjects = []
        duplicates = False
        for subject in subjects:
            added_subject, duplicate = self.add_subject(subject = subject)
            duplicates = duplicates or duplicate
            added_subjects.append(added_subject)
        return added_subjects, duplicates

    def add_subject(self, i = None, subject = None):
        if not i:
            i = len(self.subjects)
        if not subject:
            subject = self.new_subject()
        for existing_subject in self.subjects:
            if subject == existing_subject:
                return existing_subject, True
        self.subjects.insert(i, subject)
        return subject, False

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

    def invert_group_name(self, group_names):
        invert_name = "("
        for idx, name in enumerate(group_names):
            invert_name += name
            if idx < len(group_names)-1:
                invert_name += " ∪ "
            else:
                invert_name += ")'"
        return invert_name

    def invert_groups(self, group_indices):
        group_subjects = []
        group_names = []
        for group_idx in group_indices:
            group = self.groups[group_idx]
            group_subjects.extend([subject for subject in group.subjects])
            group_names.append(group.name)
        subjects = [subject for subject in self.subjects if subject not in group_subjects]
        group = Group(self.subject_class, name = self.invert_group_name(group_names), subjects = subjects, description = "Group complement")
        self.add_group(group = group)

    def merge_group_name(self, group_names):
        merge_name = ""
        for idx, name in enumerate(group_names):
            merge_name += name
            if idx < len(group_names)-1:
                merge_name += " ∪ "
        return merge_name

    def merge_groups(self, group_indices):
        if len(group_indices) < 2:
            return
        subjects = []
        group_names = []
        for group_idx in group_indices:
            group = self.groups[group_idx]
            subjects.extend([subject for subject in group.subjects if subject not in subjects])
            group_names.append(group.name)
        group = Group(self.subject_class, name = self.merge_group_name(group_names), subjects = subjects, description = "Group union")
        self.add_group(group = group)

    def intersect_group_name(self, group_names):
        intersect_name = ""
        for idx, name in enumerate(group_names):
            intersect_name += name
            if idx < len(group_names)-1:
                intersect_name += " ∩ "
        return intersect_name

    def intersect_groups(self, group_indices):
        if len(group_indices) < 2:
            return
        group = self.groups[group_indices[0]]
        subjects = set(group.subjects)
        group_names = [group.name]
        for i in range(1, len(group_indices)):
            group_idx = group_indices[i]
            group = self.groups[group_idx]
            subjects = subjects.intersection(set(group.subjects))
            group_names.append(group.name)
        subjects = list(subjects)
        group = Group(self.subject_class, name = self.intersect_group_name(group_names), subjects = subjects, description = "Group intersection")
        self.add_group(group = group)

    def load_from_file(self, file_name, subject_load_function):
        group_name = file_name.split('/')[-1]
        group = Group(self.subject_class, name = group_name)
        subjects = subject_load_function(file_name, self.atlas.brain_region_number())
        subjects, duplicates = self.add_subjects(subjects)
        group.add_subjects(subjects)
        self.add_group(group=group)
        return duplicates

    def save_to_txt(self, file_name):
        s = ""
        for label in self.atlas.get_brain_region_labels():
            s += label + " "
        for subject in self.subjects:
            s += "\n{}".format(str(subject))
        with open(file_name, 'w') as f:
            f.write(s)

    def load_from_txt(self, file_name):
        return self.load_from_file(file_name, self.subject_class.from_txt)

    def load_from_xml(self, file_name):
        return self.load_from_file(file_name, self.subject_class.from_xml)

    def load_from_xlsx(self, file_name):
        return self.load_from_file(file_name, self.subject_class.from_xlsx)
