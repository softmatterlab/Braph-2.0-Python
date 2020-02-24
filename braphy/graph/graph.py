from braphy.graph.community_algorithms import CommunityAlgorithms
from abc import ABC, abstractmethod
import numpy as np
from scipy.sparse.csgraph import dijkstra
import copy

class Graph(ABC):
    def __init__(self, A, measure_list):
        self.A = A
        self.init_measure_dict(measure_list)
        self.D = Graph.distance(self.A, self.is_weighted(), self.is_directed())
        self.community_structure, self.modularity = \
            CommunityAlgorithms.compute_community(self.A, self.is_weighted(), self.is_directed(),
                                                  'Louvain')

    def init_measure_dict(self, measure_list):
        measure_dict = {}
        for measure in measure_list:
            measure_dict[measure] = {}
        self.measure_dict = measure_dict

    def clear_community_dependent_measures(self):
        for measure in self.measure_dict.keys():
            if measure.community_dependent():
                self.measure_dict[measure] = {}

    def same_community(self, i, j):
        return self.community_structure[i] == self.community_structure[j]

    def is_weighted():
        return weighted

    def is_binary():
        return not weighted

    def is_directed():
        return directed

    def is_undirected():
        return not directed

    def is_weighted(self):
        return type(self).weighted

    def is_binary(self):
        return not type(self).weighted

    def is_directed(self):
        return type(self).directed

    def is_undirected(self):
        return not type(self).directed

    def get_measure(self, measure_class, measure = None):
        if len(self.measure_dict[measure_class]) == 0:
            measure_class.compute_measure(self)
        if measure == None:
            return self.measure_dict[measure_class]
        else:
            return self.measure_dict[measure_class][measure]

    @abstractmethod
    def is_selfconnected(self):
        pass

    @abstractmethod
    def is_nonnegative(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    def remove_diagonal(A, value = 0):
        np.fill_diagonal(A, value)
        return A

    def remove_negative_weights(A, rule):
        if rule == 'zero' or rule == '0':
            A[A < 0] = 0
        elif rule == 'null':
            A[np.isnan(A)] = 0
        else:
            A = np.abs(A)
        return A

    def symmetrize(A, rule):
        if rule == 'sum' or rule == 'add':
            A = A + A.T
        elif rule == 'av' or rule == 'average':
            A = (A + A.T) / 2
        elif rule == 'min' or rule == 'minimum' or rule == 'or' or rule == 'weak':
            A = np.minimum(A, A.T)
        else:
            A = np.maximum(A, A.T)
        return A

    def binarize(A):
        A[A != 0] = 1
        return A

    def distance(A, is_weighted, is_directed):
        if is_weighted:
            D = Graph.dijkstras(A, is_directed)
        else:
            D = Graph.breadth_first_search(A)
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
        D = A.copy()
        distance_product = A.copy()
        idx = 1
        while np.sum(idx) >= 1:
            current_length = current_length + 1
            distance_product = distance_product.dot(A)
            idx = np.zeros([len(A), len(A)], dtype = int)
            idx[(D == 0) & (distance_product != 0)] = 1
            D[idx == 1] = current_length
        D = D.astype(float)
        D[D == 0] = np.inf
        np.fill_diagonal(D, 0.0)
        return D
