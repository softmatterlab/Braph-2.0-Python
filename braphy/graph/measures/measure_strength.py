from braphy.graph.measures.measure import Measure
from braphy.graph.graphs import *
import numpy as np
import copy

class MeasureStrength(Measure):
    def dimensions():
        d = {}
        d['strength'] = Measure.NODAL
        d['avg_strength'] = Measure.GLOBAL
        d['in_strength'] = Measure.NODAL
        d['avg_in_strength'] = Measure.GLOBAL
        d['out_strength'] = Measure.NODAL
        d['avg_out_strength'] = Measure.GLOBAL
        return d

    def get_description():

        description = {}
        description['strength'] = 'The strength of a node is the sum of the weights of the edges connected to the node.'
        description['avg_strength'] = 'The average strength of a graph is the average node strength. ' +\
                                      'The node strength is the sum of the weights of the edges connected to the node.'
        description['in_strength'] = 'In directed graphs, the in-strength of a node is the sum of inward ' +\
                                     'edge weights. Connection weights are ignored in calculations.'
        description['avg_in_strength'] = 'In directed graphs, the average in-strength is the average node in-strength. ' +\
                                         'The node in-strength of a node is the sum of inward edge weights.'
        description['out_strength'] = 'In directed graphs, the out-strength of a node is the sum of outward edge weights.'
        description['avg_out_strength'] = 'In directed graphs, the average out-strength is the average node out-strength. ' +\
                                          'The node out-strength of a node is the sum of outward edge weights.'
        return description

    def compute_measure(graph):
        measure_dict = {}
        A = graph.A.copy()
        np.fill_diagonal(A, 0)

        in_strength = np.sum(A, 0)
        out_strength = np.sum(A, 1)
        strength = np.add(in_strength, out_strength)

        if graph.is_undirected():
            strength = np.multiply(strength, 0.5)
            measure_dict['strength'] = strength
            measure_dict['avg_strength'] = np.mean(strength)
        else:
            measure_dict['in_strength'] = in_strength
            measure_dict['out_strength'] = out_strength
            measure_dict['avg_in_strength'] = np.mean(in_strength)
            measure_dict['avg_out_strength'] = np.mean(out_strength)

        
        return measure_dict

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphWD] = ['in_strength', 'out_strength', 'avg_in_strength', 'avg_out_strength']
        graph_type_measures[GraphWU] = ['strength', 'avg_strength']
        return graph_type_measures
