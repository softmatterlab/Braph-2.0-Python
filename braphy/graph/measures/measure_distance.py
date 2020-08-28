from braphy.graph.measures.measure import Measure
from braphy.graph.graphs import *
from scipy.sparse.csgraph import dijkstra
import numpy as np
import copy

class MeasureDistance(Measure):
    def dimensions():
        d = {}
        d['distance'] = Measure.BINODAL
        d['edge_number_distance'] = Measure.BINODAL
        return d

    def get_description():
        description = {}
        description['distance'] = 'The distance between two nodes is defined as the length of the ' +\
                                  'shortest path between those nodes'
        description['edge_number_distance'] =  'The edge number distance of a graph is ' +\
                                               'the number of edges in the shortest weighted' +\
                                               'path between two nodes. '
        return description

    def compute_measure(graph):
        return MeasureDistance.distance(graph.A.copy(), graph.is_weighted(), graph.is_directed())

    def distance(A, is_weighted, is_directed):
        measure_dict = {}
        if is_weighted:
            distance, predecessors = MeasureDistance.weighted_distance(A, is_directed)
            edge_number_distance = MeasureDistance.edge_number_distance(predecessors)
            measure_dict['edge_number_distance'] = edge_number_distance
        else:
            distance = MeasureDistance.binary_distance(A)
        measure_dict['distance'] = distance
        return measure_dict

    def weighted_distance(A, is_directed):
        lengths = A.copy()
        lengths = lengths.astype(float)
        lengths[lengths == 0] = np.inf
        lengths = 1/lengths
        lengths[lengths == 0] = np.inf
        return dijkstra(lengths, is_directed, return_predecessors = True)

    def binary_distance(A):
        current_length = 1
        distance = A.copy()
        distance_product = A.copy()
        idx = 1
        while np.sum(idx) >= 1:
            current_length = current_length + 1
            distance_product = distance_product.dot(A)
            idx = np.zeros([len(A), len(A)], dtype = int)
            idx[(distance == 0) & (distance_product != 0)] = 1
            distance[idx == 1] = current_length
        distance = distance.astype(float)
        distance[distance == 0] = np.inf
        np.fill_diagonal(distance, 0.0)
        return distance

    def edge_number_distance(predecessors):
        edge_number_distance = np.zeros(predecessors.shape)
        for i in range(len(edge_number_distance)):
            for j in range(len(edge_number_distance)):
                if (i == j) | predecessors[i, j] == -9999:
                    continue
                number_of_edges_in_shortest_path = 1
                previous_node = predecessors[i, j]
                while (previous_node != i):
                    number_of_edges_in_shortest_path = number_of_edges_in_shortest_path + 1
                    previous_node = predecessors[i, previous_node]
                edge_number_distance[i, j] = number_of_edges_in_shortest_path
        return edge_number_distance


    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['distance']
        graph_type_measures[GraphBU] = ['distance']
        graph_type_measures[GraphWD] = ['distance', 'edge_number_distance']
        graph_type_measures[GraphWU] = ['distance', 'edge_number_distance']

        return graph_type_measures
