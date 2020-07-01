from abc import ABC, abstractmethod
import numpy as np
import copy
from braphy.graph.graphs.random_graph import RandomGraph

class Graph(ABC):
    def __init__(self, A, settings):
        self.A = A
        self.settings = settings
        self.init_measure_dict()

    def init_measure_dict(self):
        measure_dict = {}
        for measure in self.settings.measure_list:
            measure_dict[measure] = {}
        self.measure_dict = measure_dict

    def clear_community_dependent_measures(self):
        for measure in self.measure_dict.keys():
            if measure.community_dependent():
                self.measure_dict[measure] = {}

    def same_community(self, i, j):
        return self.community_structure[i] == self.community_structure[j]

    def is_weighted(self):
        return type(self).weighted

    def is_binary(self):
        return not type(self).weighted

    def is_directed(self):
        return type(self).directed

    def is_undirected(self):
        return not type(self).directed

    def get_measure(self, measure_class, measure = None, save = True):
        if len(self.measure_dict[measure_class]) == 0:
            return_value = measure_class.compute_measure(self)
            if save:
                self.measure_dict[measure_class] = return_value
        else:
            return_value = self.measure_dict[measure_class]

        if measure == None:
            return return_value
        else:
            return return_value[measure]

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

    def semipositivize(A, rule):
        if rule == 'abs' or rule == 'absolute' or rule == 'modulus':
            A = np.abs(A)
        else: # rule == zero / 0 / null
            A[A < 0] = 0
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

    def binarize(A, rule, value):
        if rule == 'density':
            assert value >=0 and value <= 1
            threshold = np.sort(A.flatten())[int(value*(np.size(A)-1))]
            A = np.where(A < threshold, 1, 0)
        elif rule == 'threshold':
            A = np.where(A >= value, 1, 0)
        return A

    def standardize(A, rule):
        if rule == 'range' or rule == 'compress':
            if np.min(A) != np.max(A):
                new_A = (A - np.min(A)) / (np.max(A) - np.min(A))
            else:
                new_A = Graph.binarize(A)
        elif rule == 'do_not_standardize':
            new_A = A
        else: # rule == threshold / one / 1
            new_A = A.copy()
            new_A[new_A < 0] = 0
            new_A[new_A > 1] = 1
        return new_A

    @abstractmethod
    def get_random_graph(self, attempts_per_edge):
        pass
