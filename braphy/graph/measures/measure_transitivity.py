from braphy.graph.measures.measure import Measure
from braphy.graph.measures.measure_triangles import MeasureTriangles
from braphy.graph.measures.measure_degree import MeasureDegree
from braphy.graph.graphs import *
import numpy as np
import copy

class MeasureTransitivity(Measure):

    def dimensions():
        d = {}
        d['transitivity'] = Measure.GLOBAL
        return d

    def get_description():
        description = {}
        description['transitivity'] = 'The transitivity is the ratio of triangles to triplets in the graph. ' +\
                                      'It is an alternative to the graph clustering coefficient.'
        return description

    def compute_measure(graph):
        measure_dict = {}
        A = graph.A.copy()
        triangles = graph.get_measure(MeasureTriangles, 'triangles', save = False)

        if graph.is_undirected(): # BU and WU
            degree = graph.get_measure(MeasureDegree, 'degree', save = False)
            transitivity = 2 * np.sum(triangles) / (np.sum((degree * (degree - 1))))
        else: # BD and WD
            in_degree = graph.get_measure(MeasureDegree, 'in_degree', save = False)
            out_degree = graph.get_measure(MeasureDegree, 'out_degree', save = False)
            transitivity = np.sum(triangles) / np.sum((((out_degree + in_degree)) * (out_degree + in_degree - 1) - 2 * np.diag(A.dot(A))))

        measure_dict['transitivity'] = transitivity
        return measure_dict

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['transitivity']
        graph_type_measures[GraphBU] = ['transitivity']
        graph_type_measures[GraphWD] = ['transitivity']
        graph_type_measures[GraphWU] = ['transitivity']

        return graph_type_measures
