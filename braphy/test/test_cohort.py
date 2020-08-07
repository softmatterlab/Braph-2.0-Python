import unittest
import numpy as np
from braphy.cohort.cohort import Cohort
from braphy.atlas.brain_atlas import BrainAtlas
from braphy.workflows import *
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.test.test_utility import TestUtility

class TestCohort(TestUtility):

    def test_read_mri(self):
        atlas = BrainAtlas()
        atlas.brain_regions = [' ']*68
        cohort = Cohort('mri', SubjectStructural, atlas)
        f = abs_path_from_relative(__file__, '../cohort/gr1_MRI.txt')
        cohort.load_from_txt(f)
        f = abs_path_from_relative(__file__, '../cohort/gr1_MRI.xml')
        cohort.load_from_xml(f)
        f = abs_path_from_relative(__file__, '../cohort/gr1_MRI.xlsx')
        cohort.load_from_xlsx(f)

    def test_read_fmri(self):
        atlas = BrainAtlas()
        atlas.brain_regions = [' ']*160
        cohort = Cohort('fmri', SubjectFunctional, atlas)
        f = abs_path_from_relative(__file__, '../cohort/gr1_fMRI.xml')
        cohort.load_from_xml(f)

if __name__ == '__main__':
    unittest.main()
