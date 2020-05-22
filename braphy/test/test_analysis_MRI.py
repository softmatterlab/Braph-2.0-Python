import unittest
from braphy.atlas.brain_atlas import BrainAtlas
from braphy.cohort.cohort import Cohort
from braphy.workflows.MRI.subject_MRI import SubjectMRI
from braphy.workflows.MRI.analysis_MRI import AnalysisMRI
from braphy.graph.measures import *
from braphy.utility.helper_functions import abs_path_from_relative
import numpy as np

class TestAnalysisMRI(unittest.TestCase):
    def test_empty_cohort(self):
        atlas = BrainAtlas()
        cohort = Cohort('mri', SubjectMRI, atlas)
        analysis = AnalysisMRI(cohort)

    def test_cohort_from_file(self):
        file = abs_path_from_relative(__file__, '../cohort/desikan_mri.cohort')
        cohort = Cohort.from_file(file)
        analysis = AnalysisMRI(cohort)

    def test_comparison(self):
        file = abs_path_from_relative(__file__, '../cohort/desikan_mri.cohort')
        cohort = Cohort.from_file(file)
        analysis = AnalysisMRI(cohort)
        comparison = analysis.get_comparison(MeasureDegree, 'degree', [0, 0])

if __name__ == '__main__':
    unittest.main()
