from braphy.graph.measures.measure import Measure
from braphy.graph.measures.measure_triangles import MeasureTriangles
from braphy.graph.measures.measure_degree import MeasureDegree
from braphy.graph.graphs import *
import numpy as np
import copy

class MeasureTransitivity(Measure):

    def dimensions():
        d = {}
        d['transitivity'] = Measure.NODAL
        return d

    def get_description():
        description = {}
        description['transitivity'] = 'The transitivity is the ratio of triangles to triplets in the graph. ' +\
                                      'It is an alternative to the graph clustering coefficient.'
        return description

    def compute_measure(graph):
        measure_dict = {}
        A = graph.A.copy()
        np.fill_diagonal(A, 0)

        if graph.is_undirected() and graph.is_binary():
            transitivity = np.sum(np.diag(A.dot(A.dot(A)))) / (np.sum(np.sum(A.dot(A))) - np.sum(np.diag(A.dot(A))))
        else:
            degree = graph.get_measure(MeasureDegree, 'degree', save = False)
            triangles = graph.get_measure(MeasureTriangles, 'triangles', save = False)
            false_connections = 0
            if graph.directed:
                false_connections = 2 * np.diag(A.dot(A))

            connected_triples = degree * (degree - 1) - false_connections

            if connected_triples.any():
                transitivity = 3 * np.sum(triangles) / np.sum(connected_triples)
            else:
                transitivity = 0

        measure_dict['transitivity'] = transitivity
        return measure_dict

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['transitivity']
        graph_type_measures[GraphBU] = ['transitivity']
        graph_type_measures[GraphWD] = ['transitivity']
        graph_type_measures[GraphWU] = ['transitivity']

        return graph_type_measures
