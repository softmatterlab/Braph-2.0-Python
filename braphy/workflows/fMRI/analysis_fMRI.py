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
        self.community_structure = {}
        for i in range(len(self.cohort.groups)):
            self.community_structure[i] = np.zeros([len(self.cohort.groups[i].subjects), self.number_of_regions()])

    def get_community_structure(self, group_index, subject_index):
        return self.community_structure[group_index][subject_index, :]

    def set_community_structure(self, group_index, community_structure, subject_index):
        self.community_structure[group_index][subject_index, :] = community_structure

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
        group_1 = self.cohort.groups[groups[0]]
        group_2 = self.cohort.groups[groups[1]]
        measures_1 = np.array(self.get_measurement(measure_class, sub_measure, groups[0]).get_value())
        measures_2 = np.array(self.get_measurement(measure_class, sub_measure, groups[1]).get_value())
        measures = np.concatenate((measures_1, measures_2))
        permutation_diffs = []
        for _ in range(permutations):
            np.random.shuffle(measures)
            permutated_measures_1 = np.array(measures[:len(measures_1)])
            permutated_measures_2 = np.array(measures[len(measures_1):])

            mean_permutated_1 = np.mean(permutated_measures_1, axis = 0)
            mean_permutated_2 = np.mean(permutated_measures_2, axis = 0)

            permutation_diffs.append(mean_permutated_2 - mean_permutated_1)

        permutation_diffs = np.array(permutation_diffs)
        difference_mean = np.mean(measures_2, axis = 0) - np.mean(measures_1, axis = 0)
        p1 = stat.p_value(difference_mean, permutation_diffs, True)
        p2 = stat.p_value(difference_mean, permutation_diffs, False)
        percentiles = None #stat.quantiles(difference_mean, 100)

        comparison = ComparisonfMRI(groups, measure_class, sub_measure, permutation_diffs, (p1, p2), (0, 0), (measures_1, measures_2), permutations)
        return comparison

    def get_graph(self, group_index):
        A = self.get_correlation(group_index)
        graphs = []
        for i in range(A.shape[0]):
            graphs.append(GraphFactory.get_graph(A[i,:,:], self.graph_settings))
        return graphs