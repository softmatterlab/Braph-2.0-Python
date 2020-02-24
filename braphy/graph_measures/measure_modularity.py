from braphy.graph_measures.measure import Measure
from braphy.graph_measures.measure_degree import MeasureDegree
from braphy.graph import *
import numpy as np
import copy

class MeasureModularity(Measure):

    def get_description():
        description = {}
        description['modularity'] = 'The modularity is a statistic that quantifies the ' +\
                                'degree to which the graph may be subdivided into such clearly delineated groups.'
        return description

    def compute_measure(graph):
        graph.measure_dict[MeasureModularity]['modularity'] = graph.modularity

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['modularity']
        graph_type_measures[GraphBU] = ['modularity']
        graph_type_measures[GraphWD] = ['modularity']
        graph_type_measures[GraphWU] = ['modularity']

        return graph_type_measures

    def community_dependent():
        return True
