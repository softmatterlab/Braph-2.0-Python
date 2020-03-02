from braphy.graph.graph_measures.measure import Measure
from braphy.graph.graphs import *
import numpy as np
import copy

class MeasureStrength(Measure):

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
        A = graph.A.copy()
        np.fill_diagonal(A, 0)

        in_strength = np.sum(A, 0)
        out_strength = np.sum(A, 1)
        strength = np.add(in_strength, out_strength)

        if graph.is_undirected():
            strength = np.multiply(strength, 0.5)
        else:
            graph.measure_dict[MeasureStrength]['in_strength'] = in_strength
            graph.measure_dict[MeasureStrength]['out_strength'] = out_strength
            graph.measure_dict[MeasureStrength]['avg_in_strength'] = np.mean(in_strength)
            graph.measure_dict[MeasureStrength]['avg_out_strength'] = np.mean(out_strength)

        graph.measure_dict[MeasureStrength]['strength'] = strength
        graph.measure_dict[MeasureStrength]['avg_strength'] = np.mean(strength)

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphWD] = ['strength', 'avg_strength']
        graph_type_measures[GraphWU] = ['strength', 'avg_strength']

        for graph_type in graph_type_measures.keys():
            if graph_type.directed:
                graph_type_measures[graph_type].extend(['in_strength', 'out_strength',
                                                        'avg_in_strength', 'avg_out_strength'])
        return graph_type_measures
