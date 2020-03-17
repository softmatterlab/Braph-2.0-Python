import unittest
import numpy as np
from braphy.cohort.cohort import Cohort
from braphy.cohort.subjects.subject_MRI import SubjectMRI
from braphy.test.test_utility import TestUtility

class TestCohort(TestUtility):

    def test_read_cohort(self):
        cohort = Cohort('mri', SubjectMRI)
        cohort.load_from_txt(file_name='gr1_MRI.txt')

if __name__ == '__main__':
    unittest.main()
