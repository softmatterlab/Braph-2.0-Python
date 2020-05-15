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

    def get_graph(self, group_index):
        A = self.cohort.groups[group_index].correlation()
        return GraphFactory.get_graph(A, self.graph_settings)
