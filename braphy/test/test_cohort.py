import unittest
import numpy as np
from braphy.cohort.cohort import Cohort
from braphy.cohort.subjects.subject_MRI import SubjectMRI
from braphy.cohort.subjects.subject_fMRI import SubjectfMRI
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.test.test_utility import TestUtility

class TestCohort(TestUtility):

    def test_read_mri(self):
        cohort = Cohort('mri', SubjectMRI)
        f = abs_path_from_relative(__file__, '../cohort/gr1_MRI.txt')
        cohort.load_from_txt(f)
        f = abs_path_from_relative(__file__, '../cohort/gr1_MRI.xml')
        cohort.load_from_xml(f)
        f = abs_path_from_relative(__file__, '../cohort/gr1_MRI.xlsx')
        cohort.load_from_xlsx(f)

    def test_read_fmri(self):
        cohort = Cohort('fmri', SubjectfMRI)
        f = abs_path_from_relative(__file__, '../cohort/gr1_fMRI.xml')
        cohort.load_from_xml(f)

if __name__ == '__main__':
    unittest.main()
