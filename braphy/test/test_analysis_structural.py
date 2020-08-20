import unittest
from braphy.atlas.brain_atlas import BrainAtlas
from braphy.cohort.cohort import Cohort
from braphy.workflows.structural.subject_structural import SubjectStructural
from braphy.workflows.structural.analysis_structural import AnalysisStructural
from braphy.graph.graph_factory import GraphSettings
from braphy.graph.measures import *
from braphy.utility.file_utility import abs_path_from_relative
import numpy as np

class TestAnalysisStructural(unittest.TestCase):
    def test_empty_cohort(self):
        atlas = BrainAtlas()
        cohort = Cohort('structural', SubjectStructural, atlas)
        analysis = AnalysisStructural(cohort, GraphSettings())

    def test_cohort_from_file(self):
        file = abs_path_from_relative(__file__, '../cohort/desikan_mri.cohort')
        cohort = Cohort.from_file(file)
        analysis = AnalysisStructural(cohort, GraphSettings())

    def test_comparison(self):
        file = abs_path_from_relative(__file__, '../cohort/desikan_mri.cohort')
        cohort = Cohort.from_file(file)
        analysis = AnalysisStructural(cohort, GraphSettings())
        comparison = analysis.get_comparison(MeasureDegree, 'avg_degree', [0, 1], 1, False)
        comparison = analysis.get_comparison(MeasureDegree, 'degree', [0, 1], 1, False)
        comparison = analysis.get_comparison(MeasureDistance, 'distance', [0, 1], 1, False)

if __name__ == '__main__':
    unittest.main()
