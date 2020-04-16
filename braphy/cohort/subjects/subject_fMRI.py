from braphy.cohort.subjects.subject import Subject
from braphy.cohort.data_types.data_scalar import DataScalar
from braphy.cohort.data_types.data_functional import DataFunctional
import xml.etree.ElementTree as ET
import numpy as np

class SubjectfMRI(Subject):
    def __init__(self, id = 'sub_id', size = 0):
        super().__init__(id = id, size = size)

    def init_data_dict(self, size):
        self.data_dict['age'] = DataScalar()
        self.data_dict['data'] = DataFunctional(size)

    def from_txt(file_txt):
        raise Exception("Not implemented")

    def from_xml(file_xml):
        subjects = []
        with open(file_xml, 'r') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            for item in root.findall('fMRICohort/fMRISubject'):
                item = item.attrib
                subject_id = item['code']
                subject = SubjectfMRI(id = subject_id)

                fmri_data = []
                data = item['data'].strip('[]')
                for v in data.split(";"):
                    fmri_data.append(v.split())
                fmri_data = np.array(fmri_data).astype(float)
                subject.data_dict['data'].set_value(fmri_data)
                subject.data_dict['age'].set_value(int(item['age']))
                subjects.append(subject)
        return subjects

    def from_xlsx(file_xlsx):
        raise Exception("Not implemented")
