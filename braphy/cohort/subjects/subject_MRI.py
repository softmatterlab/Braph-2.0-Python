from braphy.cohort.subjects.subject import Subject
from braphy.cohort.data_types.data_scalar import DataScalar
from braphy.cohort.data_types.data_structural import DataStructural
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

class SubjectMRI(Subject):
    def __init__(self, id = 'sub_id', size = 0):
        super().__init__(id = id, size = size)

    def init_data_dict(self, size):
        self.data_dict['age'] = DataScalar()
        self.data_dict['data'] = DataStructural(size)

    def __str__(self):
        s = str(self.id)
        for value in self.data_dict['data'].value:
            s += "\t{}".format(str(value))
        return s

    def from_txt(file_txt, data_length):
        subjects = []
        with open(file_txt, 'r') as f:
            for i, line in enumerate(f):
                line = line.split()
                if i == 0:
                    continue
                assert len(line) == data_length + 1, "Data does not match the brain atlas"
                subject_id = line[0]
                subject = SubjectMRI(id = subject_id)
                mri_data = np.array(line[1:]).astype(float)
                subject.data_dict['data'].set_value(mri_data)
                subjects.append(subject)
        return subjects

    def from_xml(file_xml, data_length):
        subjects = []
        with open(file_xml, 'r') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            assert root.find('MRICohort/MRISubject') != None, "Invalid file"
            for item in root.findall('MRICohort/MRISubject'):
                item = item.attrib
                for key in ['code', 'data', 'age']:
                    assert key in item.keys(), "{} missing from subject".format(key)
                subject_id = item['code']
                subject = SubjectMRI(id = subject_id)
                mri_data = np.array(item['data'].split()).astype(float)
                assert len(mri_data) == data_length, "Data does not match the brain atlas"
                subject.data_dict['age'].set_value(int(item['age']))
                subject.data_dict['data'].set_value(mri_data)
                subjects.append(subject)
        return subjects

    def from_xlsx(file_xlsx, data_length):
        subjects = []
        data = np.array(pd.read_excel(file_xlsx))
        for item in data:
            subject_id = item[0]
            subject = SubjectMRI(id = subject_id)
            try:
                mri_data = item[1:].astype(float)
            except:
                raise Exception("Invalid file")
            assert len(mri_data) == data_length, "Data does not match the brain atlas"
            subject.data_dict['data'].set_value(mri_data)
            subjects.append(subject)
        return subjects

    def to_txt(subjects, file_name, labels):
        s = ""
        for label in labels:
            s += label + " "
        for subject in subjects:
            s += "\n{}".format(str(subject))
        with open(file_name, 'w') as f:
            f.write(s)

    def to_xlsx(subjects, file_name, labels):
        data = np.array([])
        data = subjects[0].data_dict['data'].value
        subject_ids = [subjects[0].id]
        for index in range(len(subjects)-1):
            data = np.vstack((data, subjects[index+1].data_dict['data'].value))
            subject_ids.append(subjects[index+1].id)
        d = {}
        d['Label'] = subject_ids
        for index, label in enumerate(labels):
            d[label] = data[:,index]
        df = pd.DataFrame.from_dict(d)
        with open(file_name, 'w') as f:
            df.to_excel(file_name, index = None, columns = None)

    def correlation(subjects):
        data = np.array([subject.data_dict['data'].value for subject in subjects])
        return np.corrcoef(data)
