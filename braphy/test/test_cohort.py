import unittest
import numpy as np
from braphy.cohort.cohort import Cohort
from braphy.cohort.subjects.subject_MRI import SubjectMRI
from braphy.cohort.subjects.subject_fMRI import SubjectfMRI
from braphy.test.test_utility import TestUtility

class TestCohort(TestUtility):

    def test_read_mri(self):
        cohort = Cohort('mri', SubjectMRI)
        cohort.load_from_txt(file_name='gr1_MRI.txt')
        cohort.load_from_xml(file_name='gr1_MRI.xml')
        cohort.load_from_xlsx(file_name='gr1_MRI.xlsx')

    def test_read_fmri(self):
        cohort = Cohort('fmri', SubjectfMRI)
        cohort.load_from_xml(file_name='gr1_fMRI.xml')

if __name__ == '__main__':
    unittest.main()
