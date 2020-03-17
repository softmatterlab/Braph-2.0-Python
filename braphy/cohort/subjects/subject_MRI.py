from braphy.cohort.subjects.subject import Subject
from braphy.cohort.data_types.data_scalar import DataScalar
from braphy.cohort.data_types.data_structural import DataStructural
import xml.etree.ElementTree as ET
import numpy as np

class SubjectMRI(Subject):
    def __init__(self, id = 'sub_id'):
        super().__init__(id = id)

    def init_data_dict(self):
        self.data_dict['age'] = DataScalar()
        self.data_dict['MRI'] = DataStructural()

    def from_txt(file_txt):
        subjects = []
        with open(file_txt, 'r') as f:
            for i, line in enumerate(f):
                line = line.split()
                if i == 0:
                    continue
                subject_id = line[0]
                subject = SubjectMRI(id = subject_id)
                mri_data = np.array(line[1:]).astype(float)
                subject.data_dict['MRI'].set_value(mri_data)
                subjects.append(subject)
        return subjects

    def from_xml(file_xml):
        subjects = []
        with open(file_xml, 'r') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            for item in root.findall('MRICohort/MRISubject'):
                item = item.attrib
                subject_id = item['code']
                subject = SubjectMRI(id = subject_id)
                mri_data = np.array(item['data'].split()).astype(float)
                subject.data_dict['age'].set_value(int(item['age']))
                subject.data_dict['MRI'].set_value(mri_data)
                subjects.append(subject)
        return subjects
