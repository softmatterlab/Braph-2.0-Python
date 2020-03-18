class Group:
    def __init__(self, subject_class, subjects = [], name = 'Group', description = '-'):
        self.name = name
        self.description = description
        self.subject_class = subject_class
        self.subjects = subjects

    def add_subject(self, subjects):
        self.subjects.append(subjects)

    def add_subjects(self, subjects):
        self.subjects.extend(subjects)

    def remove_subject(self, subjects):
        self.subjects.remove(subjects)

    def remove_subjects(self, subjects):
        for subject in subjects:
            self.subjects.remove(subject)
