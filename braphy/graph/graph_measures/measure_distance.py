from braphy.graph.graph_measures.measure import Measure
from braphy.graph.graphs import *
import numpy as np
import copy

class MeasureDistance(Measure):

    def get_description():

        description = {}
        description['distance'] = 'distance'
        return description

    def compute_measure(graph):
        distance = MeasureDistance.distance(graph.A, graph.is_weighted(), graph.is_directed())
        graph.measure_dict[MeasureDistance]['distance'] = distance

    def distance(A, is_weighted, is_directed):
        if is_weighted:
            D = MeasureDistance.dijkstras(A, is_directed)
        else:
            D = MeasureDistance.breadth_first_search(A)
        return D

    def dijkstras(A, is_directed):
        lengths = A.copy()
        lengths = lengths.astype(float)
        lengths[lengths == 0] = np.inf
        lengths = 1/lengths
        lengths[lengths == 0] = np.inf
        return dijkstra(lengths, is_directed)

    def breadth_first_search(A):
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

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['distance']
        graph_type_measures[GraphBU] = ['distance']
        graph_type_measures[GraphWD] = ['distance']
        graph_type_measures[GraphWU] = ['distance']

        return graph_type_measures