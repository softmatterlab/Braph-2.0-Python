from braphy.graph.graph_factory import GraphFactory, GraphSettings
import numpy as np

class Analysis():
    def __init__(self, cohort, name = 'analysis'):
        self.cohort = cohort
        self.name = name
        self.graph_settings = GraphSettings.get_bd()

    def set_name(self, name):
        self.name = name

    def set_graph_type(self, graph_type):
        self.graph_settings.weighted = graph_type.weighted
        self.graph_settings.directed = graph_type.directed

    def set_correlation(self, correlation_type):
        pass

    def set_negative_rule(self, negative_rule):
        self.graph_settings.rule_semipositivize = negative_rule

    def get_correlation(self, group_index):
        return self.cohort.groups[group_index].correlation()

    def correlation_threshold(self, A, threshold):
        return np.where(A > threshold, 1, 0)

    def correlation_density(self, A, density):
        assert density >=0 and density <= 1
        threshold = np.sort(A.flatten())[int(density*(np.size(A)-1))]
        return self.correlation_threshold(A, threshold)

    def get_graph(self, group_index):
        A = self.get_correlation(group_index)
        return GraphFactory.get_graph(A, self.graph_settings)

