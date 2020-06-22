from braphy.analysis.analysis import Analysis
from braphy.workflows.MRI.measurement_MRI import MeasurementMRI
from braphy.workflows.MRI.comparison_MRI import ComparisonMRI
from braphy.graph.measures.measure_community_structure import MeasureCommunityStructure
from braphy.utility.permutation import Permutation
from braphy.utility.stat_functions import StatFunctions as stat
from braphy.graph.graph_factory import GraphFactory
import numpy as np
class AnalysisMRI(Analysis):
    def __init__(self, cohort, graph_settings, name = 'analysis', measurements = None, random_comparisons = None, comparisons = None):
        super().__init__(cohort, graph_settings, name, measurements, random_comparisons, comparisons)
        self.community_structure = {}
        for i in range(len(self.cohort.groups)):
            self.community_structure[i] = np.zeros(self.number_of_regions())

    def number_of_communities(self, group_index):
        return np.max(self.community_structure[group_index]) +1

    def get_community_structure(self, group_index):
        return self.community_structure[group_index]

    def set_community_structure(self, group_index, community_structure):
        self.community_structure[group_index] = community_structure

    def calculate_measurement(self, measure_class, sub_measure, group_index):
        graph = self.get_graph(group_index)
        value = graph.get_measure(measure_class, sub_measure, save = False)

        measurement = MeasurementMRI(group_index, measure_class, sub_measure, value)
        return measurement

    def calculate_random_comparison(self, measure_class, sub_measure, group):
        pass

    def calculate_comparison(self, measure_class, sub_measure, groups, permutations = 1000):
        #is_longitudinal = False
        group_1 = self.cohort.groups[groups[0]]
        group_2 = self.cohort.groups[groups[1]]
        measure_1 = self.get_measurement(measure_class, sub_measure, groups[0]).get_value()
        measure_2 = self.get_measurement(measure_class, sub_measure, groups[1]).get_value()
        permutation_diffs = []
        for _ in range(permutations):
            permutated_subjects_1, permutated_subjects_2 = Permutation.permute(np.array(group_1.subjects), np.array(group_2.subjects), True)

            A_permutated_1 = group_1.subject_class.correlation(permutated_subjects_1, self.graph_settings.correlation_type)
            graph_permutated_1 = GraphFactory.get_graph(A_permutated_1, self.graph_settings)
            measure_permutated_1 = graph_permutated_1.get_measure(measure_class, sub_measure, False)

            A_permutated_2 = group_2.subject_class.correlation(permutated_subjects_2, self.graph_settings.correlation_type)
            graph_permutated_2 = GraphFactory.get_graph(A_permutated_2, self.graph_settings)
            measure_permutated_2 = graph_permutated_2.get_measure(measure_class, sub_measure, False)

            permutation_diffs.append(measure_permutated_2 - measure_permutated_1)

        permutation_diffs = np.array(permutation_diffs)
        difference_mean = measure_2 - measure_1
        p1 = stat.p_value(difference_mean, permutation_diffs, True)
        p2 = stat.p_value(difference_mean, permutation_diffs, False)
        percentiles = None #stat.quantiles(difference_mean, 100)

        comparison = ComparisonMRI(groups, measure_class, sub_measure, permutation_diffs, (p1, p2), (0, 0), (measure_1, measure_2), permutations)
        return comparison

    def get_graph(self, group_index):
        A = self.get_correlation(group_index)
        return GraphFactory.get_graph(A, self.graph_settings)

    def calculate_community_structure(self, group_index):
        return self.get_graph(group_index).get_measure(MeasureCommunityStructure, 'community_structure')
