from braphy.cohort.subjects.subject import Subject
from braphy.cohort.data_types.data_scalar import DataScalar
from braphy.cohort.data_types.data_functional import DataFunctional
from braphy.utility.helper_functions import float_to_string
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

class SubjectfMRI(Subject):
    def __init__(self, id = 'sub_id', size = 0):
        super().__init__(id = id, size = size)

    def init_data_dict(self, size):
        self.data_dict['age'] = DataScalar()
        self.data_dict['data'] = DataFunctional(size)

    def __str__(self):
        s = ''
        for row in range(self.data_dict['data'].value.shape[0]):
            data_row = self.data_dict['data'].value[row, :]
            data_row_string = [float_to_string(data) for data in data_row]
            s += "{}\n".format(' '.join(data_row_string))
        return s

    def from_txt(file_txt, data_length):
        raise Exception("Not implemented")

    def from_xml(file_xml, data_length):
        subjects = []
        with open(file_xml, 'r') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            assert root.find('fMRICohort/fMRISubject') != None, "Could not find any subjects in file"
            for item in root.findall('fMRICohort/fMRISubject'):
                item = item.attrib
                subject_id = item['code']
                subject = SubjectfMRI(id = subject_id)
                fmri_data = []
                data = item['data'].strip('[]')
                for v in data.split(";"):
                    fmri_data.append(v.split())
                fmri_data = np.array(fmri_data).astype(float)
                assert np.shape(fmri_data)[1] == data_length, "Data does not match the brain atlas"
                subject.data_dict['data'].set_value(fmri_data)
                subject.data_dict['age'].set_value(int(item['age']))
                subjects.append(subject)
        return subjects

    def from_xlsx(file_xlsx, data_length):
        subject_id = file_xlsx.split('/')[-1].split('.')[0]
        subject = SubjectfMRI(id = subject_id)
        data = pd.read_excel(file_xlsx)
        first_row = np.array(data.columns)
        data = np.vstack([first_row, np.array(data)])
        #assert np.size(data, 1) == data_length
        subject.data_dict['data'].set_value(data)
        return [subject]
