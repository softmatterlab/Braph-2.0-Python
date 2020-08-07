from braphy.cohort.subject import Subject
from braphy.cohort.data_types.data_scalar import DataScalar
from braphy.cohort.data_types.data_functional import DataFunctional
from braphy.utility.helper_functions import float_to_string
from braphy.utility.stat_functions import StatFunctions
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

class SubjectFunctional(Subject):
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
        raise Exception("Loading functional subject from txt not yet implemented")

    def from_xml(file_xml, data_length):
        subjects = []
        with open(file_xml, 'r') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            functional = 'FunctionalCohort/FunctionalSubject'
            fmri = 'fMRICohort/fMRISubject'
            functional_found = root.find(functional)
            fmri_found = root.find(fmri)
            assert (functional_found or fmri_found) is not None, "Invalid file"
            for item in (root.findall(functional) + root.findall(fmri)):
                item = item.attrib
                subject_id = item['code']
                subject = SubjectFunctional(id = subject_id)
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

    def from_xlsx(files_xlsx, data_length):
        subjects = []
        if not isinstance(files_xlsx, list):
            files_xlsx = [files_xlsx]
        for file_xlsx in files_xlsx:
            subject_id = file_xlsx.split('/')[-1].split('.')[0]
            subject = SubjectFunctional(id = subject_id)
            data = pd.read_excel(file_xlsx)
            first_row = np.array(data.columns)
            data = np.vstack([first_row, np.array(data)])
            if not np.size(data, 1) == data_length:
                continue
            subject.data_dict['data'].set_value(data)
            subjects.append(subject)
        assert len(subjects) > 0, 'Data does not match the brain atlas'
        return subjects

    def to_txt(subjects, file_path, labels):
        labels = ' '.join(labels)
        s = ''
        for subject in subjects:
            s += '{}\n{}\n{}'.format(subject.id, labels, str(subject))
            file_name = '{}/{}.txt'.format(file_path, subject.id)
            with open(file_name, 'w') as f:
                f.write(s)
            s = ''

    def to_xlsx(subjects, file_path, labels):
        for subject in subjects:
            data = subject.data_dict['data'].value
            d = {}
            for index, label in enumerate(labels):
                d[label] = data[:,index]
            df = pd.DataFrame.from_dict(d)
            file_name = '{}/{}.xlsx'.format(file_path, subject.id)
            with open(file_name, 'w') as f:
                df.to_excel(file_name, index = None, columns = None, header = False)

    def correlation(subjects, correlation_type):
        if isinstance(subjects, np.ndarray):
            subjects = subjects.tolist()
        correlations = []
        for subject in subjects:
            data = subject.data_dict['data'].value.T
            correlations.append(StatFunctions.correlation(data, correlation_type))
        return np.array(correlations)

    def functional():
        return True

    def structural():
        return False
