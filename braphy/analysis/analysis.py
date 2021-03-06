from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.graphs.graph import Graph
from braphy.cohort.cohort import Cohort
from braphy.analysis.measurement import Measurement
from braphy.analysis.comparison import Comparison
from braphy.analysis.random_comparison import RandomComparison
from braphy.utility.helper_functions import same_class, analysis_subject_match
import numpy as np
from abc import ABC, abstractmethod

class Analysis():
    def __init__(self, cohort, graph_settings, name = 'analysis', measurements = None, random_comparisons = None, comparisons = None):
        self.cohort = cohort
        self.name = name
        self.graph_settings = graph_settings

        self.measurements = measurements if measurements else []
        self.random_comparisons = random_comparisons if random_comparisons else []
        self.comparisons = comparisons if comparisons else []

        self.set_default_community_structure()

    def to_dict(self):
        d = {}
        d['cohort'] = self.cohort.to_dict()
        d['name'] = self.name
        d['graph_settings'] = self.graph_settings.to_dict()
        d['measurements'] = [measurement.to_dict() for measurement in self.measurements]
        d['random_comparisons'] = [random_comparison.to_dict() for random_comparison in self.random_comparisons]
        d['comparisons'] = [comparison.to_dict() for comparison in self.comparisons]
        return d

    @classmethod
    def from_dict(cls, d):
        cohort = Cohort.from_dict(d['cohort'])
        assert analysis_subject_match(cls, cohort.subject_class), \
                'Wrong data type. Subjects in cohort of type {} does not match analysis of type {}'.format(cohort.subject_class.__name__, cls.__name__)
        name = d['name']
        graph_settings = GraphSettings.from_dict(d['graph_settings'])
        measurements = [Measurement.from_dict(measurement) for measurement in d['measurements']]
        random_comparisons = [RandomComparison.from_dict(random_comparison) for random_comparison in d['random_comparisons']]
        comparisons = [Comparison.from_dict(comparison) for comparison in d['comparisons']]
        return cls(cohort, graph_settings, name, measurements, random_comparisons, comparisons)

    def structural(self):
        return self.cohort.subject_class.structural()

    def functional(self):
        return self.cohort.subject_class.functional()

    def is_weighted(self):
        return self.graph_settings.weighted

    def is_binary(self):
        return not self.graph_settings.weighted

    def number_of_regions(self):
        return len(self.cohort.atlas.brain_regions)

    def number_of_groups(self):
        return len(self.cohort.groups)

    @abstractmethod
    def number_of_communities(self, group_index):
        pass

    @abstractmethod
    def set_default_community_structure(self):
        pass

    def set_name(self, name):
        self.name = name

    def get_gamma(self):
        return self.graph_settings.gamma

    def set_gamma(self, gamma):
        assert gamma >= 0 and gamma <= 1
        self.graph_settings.gamma = gamma

    def get_binary_value(self):
        return self.graph_settings.value_binary

    def set_binary_value(self, value):
        assert value >= 0 and value <= 1
        self.graph_settings.value_binary = value

    def set_weighted(self, weighted):
        assert isinstance(weighted, bool)
        self.graph_settings.weighted = weighted

    def set_directed(self, directed):
        assert isinstance(directed, bool)
        self.graph_settings.directed = directed

    def get_measurement(self, measure_class, sub_measure, group):
        measurement = None
        check_measurement = Measurement(group, measure_class, sub_measure, binary_value = self.graph_settings.value_binary)
        for m in self.measurements:
            if m.equal(check_measurement):
                measurement = m
                break
        if not measurement:
            measurement = self.calculate_measurement(measure_class, sub_measure, group)
            self.measurements.append(measurement)
        return measurement

    def get_random_comparison(self, measure_class, sub_measure, group, attempts_per_edge, number_of_weights, randomization_number):
        random_comparison = None
        check_random_comparison = RandomComparison(measure_class, sub_measure, group, attempts_per_edge,
                                                   number_of_weights, randomization_number, 0, 0, 0, [],
                                                   (0,0), (0,0), self.graph_settings.value_binary)
        for c in self.random_comparisons:
            if (c.equal(check_random_comparison)):
                random_comparison = c
                break
        if not random_comparison:
            random_comparison = self.calculate_random_comparison(measure_class, sub_measure, group, randomization_number, number_of_weights, attempts_per_edge)
            self.random_comparisons.append(random_comparison)
        return random_comparison

    def get_comparison(self, measure_class, sub_measure, groups, permutations, longitudinal):
        comparison = None
        check_comparison = Comparison(groups, measure_class, sub_measure,
                                      permutations = permutations, binary_value = self.graph_settings.value_binary)
        for c in self.comparisons:
            if (c.equal(check_comparison)):
                comparison = c
                break
        if not comparison:
            comparison = self.calculate_comparison(measure_class, sub_measure, groups, permutations, longitudinal)
            self.comparisons.append(comparison)
        return comparison

    @abstractmethod
    def calculate_measurement(self, measure_code, group_index):
        pass

    @abstractmethod
    def calculate_random_comparison(self, measure_code, group_index):
        pass

    @abstractmethod
    def calculate_comparison(self, measure_class, sub_measure, groups, permutations, longitudinal):
        pass

    def set_correlation(self, correlation_type):
        self.graph_settings.correlation_type = correlation_type

    def set_negative_rule(self, negative_rule):
        self.graph_settings.rule_negative = negative_rule

    def set_binary_rule(self, binary_rule):
        self.graph_settings.rule_binary = binary_rule

    def set_symmetrize_rule(self, symmetrize_rule):
        self.graph_settings.rule_symmetrize = symmetrize_rule

    def set_standardize_rule(self, standardize_rule):
        self.graph_settings.rule_standardize = standardize_rule

    @abstractmethod
    def calculate_community_structure(self, group_index):
        pass

    def get_correlation(self, group_index):
        return self.cohort.groups[group_index].correlation(self.graph_settings.correlation_type)

    def correlation_threshold(self, A, threshold):
        return Graph.binarize(A, 'threshold', threshold)

    def correlation_density(self, A, density):
        return Graph.binarize(A, 'density', density)

    @abstractmethod
    def get_graph(self, group_index):
        pass

    def get_subgraph_analysis(self, selected_nodes):
        cohort = self.cohort.get_subgraph_cohort(selected_nodes)
        analysis = self.__class__(cohort, self.graph_settings, 'subgraph analysis')
        return analysis

    def binary_type(self):
        binary_type = '' if self.graph_settings.weighted else self.graph_settings.rule_binary
        return binary_type
