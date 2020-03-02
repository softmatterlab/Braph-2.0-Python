from braphy.graph.graph_measures.measure import Measure
from braphy.graph.graph_measures.measure_distance import MeasureDistance
from braphy.graph.graphs import *
import numpy as np
import copy

class MeasureEccentricity(Measure):

    def get_description():
        description = {}

        description['eccentricity'] = 'The node eccentricity is the maximal shortest ' +\
                                      'path length between a node and any other node.'

        description['avg_eccentricity'] = 'The average eccentricity is the average node eccentricy.'

        description['radius'] = 'The radius is the minimum eccentricity.'

        description['diameter'] = 'The diameter is the maximum eccentricity.'

        description['in_eccentricity'] = 'In directed graphs, the node in-eccentricity is the maximal '+\
                                         'shortest path length from any nodes in the netwrok and a node.'

        description['avg_in_eccentricity'] = 'In directed graphs, the average in-eccentricity is the average node in-eccentricy.'

        description['out_eccentricity'] = 'In directed graphs, the node out-eccentricity is the maximal shortest '+\
                                          'path length from a node to all other nodes in the netwrok.'

        description['avg_out_eccentricity'] = 'In directed graphs, the average out-eccentricity is the average node out-eccentricy.'

        return description

    def compute_measure(graph):
        measure_dict = {}
        D = graph.get_measure(MeasureDistance, 'distance', save = False).copy()
        np.fill_diagonal(D, 0)
        in_eccentricity = np.amax(np.multiply(D, D!=np.inf), axis=0)
        out_eccentricity = np.amax(np.multiply(D, D!=np.inf), axis=1)
        eccentricity = np.maximum(in_eccentricity, out_eccentricity)

        measure_dict['eccentricity'] = eccentricity
        measure_dict['avg_eccentricity'] = np.mean(eccentricity)
        measure_dict['radius'] = np.min(eccentricity)
        measure_dict['diameter'] = np.max(eccentricity)

        if graph.is_directed():
            measure_dict['in_eccentricity'] = in_eccentricity
            measure_dict['avg_in_eccentricity'] = np.mean(in_eccentricity)
            measure_dict['out_eccentricity'] = out_eccentricity
            measure_dict['avg_out_eccentricity'] = np.mean(out_eccentricity)

        return measure_dict

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['eccentricity', 'avg_eccentricity', 'radius', 'diameter']
        graph_type_measures[GraphBU] = ['eccentricity', 'avg_eccentricity', 'radius', 'diameter']
        graph_type_measures[GraphWD] = ['eccentricity', 'avg_eccentricity', 'radius', 'diameter']
        graph_type_measures[GraphWU] = ['eccentricity', 'avg_eccentricity', 'radius', 'diameter']

        for graph_type in graph_type_measures.keys():
            if graph_type.directed:
                graph_type_measures[graph_type].extend(['in_eccentricity', 'avg_in_eccentricity',
                                                        'out_eccentricity', 'avg_out_eccentricity'])

        return graph_type_measures
