from braphy.analysis.analysis import Analysis
from braphy.workflows.fMRI.measurement_fMRI import MeasurementfMRI
from braphy.workflows.fMRI.comparison_fMRI import ComparisonfMRI
from braphy.utility.permutation import Permutation
from braphy.utility.stat_functions import StatFunctions as stat
from braphy.graph.graph_factory import GraphFactory
import numpy as np

class AnalysisfMRI(Analysis):
    def __init__(self, cohort, name = 'analysis', measurements = None, random_comparisons = None, comparisons = None):
        super().__init__(cohort, name, measurements, random_comparisons, comparisons)

    def calculate_measurement(self, measure_class, sub_measure, group_index):
        graphs = self.get_graph(group_index)
        values = []
        for graph in graphs:
            values.append(graph.get_measure(measure_class, sub_measure, save = False))
        measurement = MeasurementfMRI(group_index, measure_class, sub_measure, values)
        return measurement

    def calculate_random_comparison(self, measure_class, sub_measure, group):
        pass

    def calculate_comparison(self, measure_class, sub_measure, groups, permutations = 1000):
        pass

    def get_graph(self, group_index):
        A = self.get_correlation(group_index)
        graphs = []
        for i in range(A.shape[0]):
            graphs.append(GraphFactory.get_graph(A[i,:,:], self.graph_settings))
        return graphs