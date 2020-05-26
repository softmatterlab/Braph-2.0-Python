from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_community_structure import MeasureCommunityStructure
import numpy as np
from abc import ABC, abstractmethod

class Analysis():
    def __init__(self, cohort, name = 'analysis', measurements = None, random_comparisons = None, comparisons = None):
        self.cohort = cohort
        self.name = name
        self.graph_settings = GraphSettings.get_bd()
        self.community_structure = [0]*len(self.cohort.atlas.brain_regions)

        self.measurements = measurements if measurements else []
        self.random_comparisons = random_comparisons if random_comparisons else []
        self.comparisons = comparisons if comparisons else []

    def number_of_communities(self):
        return max(self.community_structure) + 1

    def set_name(self, name):
        self.name = name

    def get_gamma(self):
        return self.graph_settings.gamma

    def set_gamma(self, gamma):
        assert gamma >= 0 and gamma <= 1
        self.graph_settings.gamma = gamma

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

    def get_comparison(self, measure_class, sub_measure, groups):
        comparison = None
        for c in self.comparisons:
            if (c.measure_class == measure_class and
                c.sub_measure == sub_measure and
                c.groups[0] == groups[0] and
                c.groups[1] == groups[1]):
                comparison = c
                break
        if not comparison:
            comparison = self.calculate_comparison(measure_class, sub_measure, groups)
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

    def get_community_structure(self, group_index):
        return self.get_graph(group_index).get_measure(MeasureCommunityStructure, 'community_structure')

    def get_correlation(self, group_index):
        return self.cohort.groups[group_index].correlation()

    def correlation_threshold(self, A, threshold):
        return np.where(A > threshold, 1, 0)

    def correlation_density(self, A, density):
        assert density >=0 and density <= 1
        threshold = np.sort(A.flatten())[int(density*(np.size(A)-1))]
        return self.correlation_threshold(A, threshold)

    @abstractmethod
    def get_graph(self, group_index):
        pass

