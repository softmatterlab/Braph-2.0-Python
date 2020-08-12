from braphy.analysis.analysis import Analysis
from braphy.workflows.functional.measurement_functional import MeasurementFunctional
from braphy.workflows.functional.comparison_functional import ComparisonFunctional
from braphy.workflows.functional.random_comparison_functional import RandomComparisonFunctional
from braphy.graph.measures.measure_community_structure import MeasureCommunityStructure
from braphy.utility.permutation import Permutation
from braphy.utility.stat_functions import StatFunctions as stat
from braphy.graph.graph_factory import GraphFactory
import numpy as np

class AnalysisFunctional(Analysis):
    def __init__(self, cohort, graph_settings, name = 'analysis', measurements = None, random_comparisons = None, comparisons = None):
        super().__init__(cohort, graph_settings, name, measurements, random_comparisons, comparisons)

    def number_of_communities(self, group_index):
        return np.max(self.community_structure[group_index], axis = 1) +1

    def get_community_structure(self, group_index, subject_index):
        return self.community_structure[group_index][subject_index, :]

    def set_community_structure(self, group_index, community_structure, subject_index = None):
        if subject_index is None:
            for subject_index in range(len(self.cohort.groups[group_index].subjects)):
                self.community_structure[group_index][subject_index, :] = community_structure
        else:
            self.community_structure[group_index][subject_index, :] = community_structure

    def calculate_measurement(self, measure_class, sub_measure, group_index):
        graphs = self.get_graph(group_index)
        values = []
        for graph in graphs:
            values.append(graph.get_measure(measure_class, sub_measure, save = False))
        measurement = MeasurementFunctional(group_index, measure_class, sub_measure, values, self.graph_settings.value_binary)
        return measurement

    def calculate_random_comparison(self, measure_class, sub_measure, group_index,
                                    randomization_number, number_of_weights, attempts_per_edge):
        graphs = self.get_graph(group_index)
        measures = np.array(self.get_measurement(measure_class, sub_measure, group_index).get_value())
        mean_measures = np.mean(measures, axis = 0)
        differences = []
        mean_random_measures = 0
        for _ in range(randomization_number):
            random_measures = []
            for graph in graphs:
                random_A = graph.get_random_graph(attempts_per_edge, number_of_weights)
                random_graph = GraphFactory.get_graph(random_A, self.graph_settings)
                random_measure = np.array(random_graph.get_measure(measure_class, sub_measure, save = False))
                random_measures.append(random_measure)
            differences.append(mean_measures - np.mean(random_measures, axis = 0))
            mean_random_measures += np.mean(random_measures, axis = 0)

        mean_random_measures = mean_random_measures / randomization_number
        difference = mean_measures - mean_random_measures
        differences = np.array(differences)
        p1 = stat.p_value(difference, differences, True)
        p2 = stat.p_value(difference, differences, False)
        quantiles = stat.quantiles(differences, 41)
        CI_lower = quantiles[1]
        CI_upper = quantiles[39]

        random_comparison = RandomComparisonFunctional(group_index, measure_class, sub_measure,
                                                       attempts_per_edge, number_of_weights,
                                                       randomization_number, mean_measures, mean_random_measures,
                                                       difference, differences, (p1, p2),
                                                       (CI_lower, CI_upper), self.graph_settings.value_binary)
        return random_comparison

    def calculate_comparison(self, measure_class, sub_measure, groups, permutations = 1000, longitudinal = False):
        group_1 = self.cohort.groups[groups[0]]
        group_2 = self.cohort.groups[groups[1]]
        measures_1 = np.array(self.get_measurement(measure_class, sub_measure, groups[0]).get_value())
        measures_2 = np.array(self.get_measurement(measure_class, sub_measure, groups[1]).get_value())
        permutation_diffs = []
        for _ in range(permutations):
            permutated_measures_1, permutated_measures_2 = Permutation.permute(measures_1, measures_2, longitudinal)

            mean_permutated_1 = np.mean(permutated_measures_1, axis = 0)
            mean_permutated_2 = np.mean(permutated_measures_2, axis = 0)

            permutation_diffs.append(mean_permutated_2 - mean_permutated_1)

        permutation_diffs = np.array(permutation_diffs)
        difference_mean = np.mean(measures_2, axis = 0) - np.mean(measures_1, axis = 0)
        p1 = stat.p_value(difference_mean, permutation_diffs, True)
        p2 = stat.p_value(difference_mean, permutation_diffs, False)
        quantiles = stat.quantiles(permutation_diffs, 41)
        CI_lower = quantiles[1]
        CI_upper = quantiles[39]
        comparison = ComparisonFunctional(groups, measure_class, sub_measure, permutation_diffs,
                                    (p1, p2), (CI_lower, CI_upper), (measures_1, measures_2), permutations, self.graph_settings.value_binary, longitudinal)
        return comparison

    def get_graph(self, group_index):
        A = self.get_correlation(group_index)
        graphs = []
        for i in range(A.shape[0]):
            graphs.append(GraphFactory.get_graph(A[i,:,:], self.graph_settings))
        return graphs

    def calculate_community_structure(self, group_index, subject_index = None):
        graphs = self.get_graph(group_index)
        if subject_index is not None:
            return graphs[subject_index].get_measure(MeasureCommunityStructure, 'community_structure')
        else:
            A = np.mean([graph.A for graph in graphs], axis = 0)
            graph = GraphFactory.get_graph(A, self.graph_settings)
            return graph.get_measure(MeasureCommunityStructure, 'community_structure')

    def set_default_community_structure(self):
        self.community_structure = {}
        for i in range(len(self.cohort.groups)):
            self.community_structure[i] = np.zeros([len(self.cohort.groups[i].subjects), self.number_of_regions()])
