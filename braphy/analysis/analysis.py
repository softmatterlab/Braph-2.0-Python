from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.graphs.graph import Graph
import numpy as np
from abc import ABC, abstractmethod

class Analysis():
    def __init__(self, cohort, name = 'analysis', measurements = None, random_comparisons = None, comparisons = None):
        self.cohort = cohort
        self.name = name
        self.graph_settings = GraphSettings.get_wd()

        self.measurements = measurements if measurements else []
        self.random_comparisons = random_comparisons if random_comparisons else []
        self.comparisons = comparisons if comparisons else []

    def number_of_regions(self):
        return len(self.cohort.atlas.brain_regions)

    def number_of_groups(self):
        return len(self.cohort.groups)

    @abstractmethod
    def number_of_communities(self, group_index):
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

    def set_graph_type(self, graph_type):
        self.graph_settings.weighted = graph_type.weighted
        self.graph_settings.directed = graph_type.directed

    def get_measurement(self, measure_class, sub_measure, group):
        measurement = None
        for m in self.measurements:
            if (m.measure_class == measure_class and
                m.sub_measure == sub_measure and
                m.group == group):
                measurement = m
                break
        if not measurement:
            measurement = self.calculate_measurement(measure_class, sub_measure, group)
            self.measurements.append(measurement)
        return measurement

    def get_random_comparison(self, measure_class, sub_measure, group):
        measurement = None
        for m in self.measurements:
            if (m.measure_class == measure_class and
                m.sub_measure == sub_measure and
                m.group == group):
                measurement = m
                break
        if not measurement:
            measurement = self.calculate_measurement(measure_class, sub_measure, group)
            self.measurements.append(measurement)
        return measurement

    def get_comparison(self, measure_class, sub_measure, groups, permutations):
        comparison = None
        for c in self.comparisons:
            if (c.measure_class == measure_class and
                c.sub_measure == sub_measure and
                c.groups[0] == groups[0] and
                c.groups[1] == groups[1] and
                c.permutations == permutations):
                comparison = c
                break
        if not comparison:
            comparison = self.calculate_comparison(measure_class, sub_measure, groups, permutations)
            self.comparisons.append(comparison)
        return comparison

    @abstractmethod
    def calculate_measurement(self, measure_code, group_index):
        pass

    @abstractmethod
    def calculate_random_comparison(self, measure_code, group_index):
        pass

    @abstractmethod
    def calculate_comparison(self, measure_code, group_index):
        pass

    def set_correlation(self, correlation_type):
        pass

    def set_negative_rule(self, negative_rule):
        self.graph_settings.rule_semipositivize = negative_rule

    def set_binary_rule(self, binary_rule):
        self.graph_settings.rule_binary = binary_rule

    @abstractmethod
    def calculate_community_structure(self, group_index):
        pass

    def get_correlation(self, group_index):
        return self.cohort.groups[group_index].correlation()

    def correlation_threshold(self, A, threshold):
        return Graph.binarize(A, 'threshold', threshold)

    def correlation_density(self, A, density):
        return Graph.binarize(A, 'density', density)

    @abstractmethod
    def get_graph(self, group_index):
        pass

