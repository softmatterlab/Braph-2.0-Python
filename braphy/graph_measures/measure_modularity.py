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
        '''
        degree = graph.get_measure(MeasureDegree, 'degree')
        number_of_edges = np.sum(graph.A)
        if graph.is_undirected():
            number_of_edges = np.multiply(number_of_edges, 0.5)

        modularity_sum = 0
        for (i, j), edge in np.ndenumerate(graph.A):
            same_community = 0
            if graph.same_community(i, j):
                same_community = 1
            modularity_sum += (edge - degree[i]*degree[j]/number_of_edges)*same_community
        modularity = modularity_sum/number_of_edges
        '''
        graph.measure_dict[MeasureModularity]['modularity'] = graph.modularity

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['modularity']
        graph_type_measures[GraphBU] = ['modularity']
        graph_type_measures[GraphWD] = ['modularity']
        graph_type_measures[GraphWU] = ['modularity']

        return graph_type_measures
