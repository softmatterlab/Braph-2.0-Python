from braphy.graph.measures.measure import Measure
from braphy.graph.graphs import *
import numpy as np
import copy

class MeasureDegree(Measure):
    def dimensions():
        d = {}
        d['degree'] = Measure.NODAL
        d['avg_degree'] = Measure.GLOBAL
        d['in_degree'] = Measure.NODAL
        d['avg_in_degree'] = Measure.GLOBAL
        d['out_degree'] = Measure.NODAL
        d['avg_out_degree'] = Measure.GLOBAL
        return d

    def get_description():

        description = {}

        description['degree'] = 'The degree of a node is the number of edges connected ' +\
                                'to the node. Connection weights are ignored in calculations.'

        description['avg_degree'] = 'The average degree of a graph is the average node degree. ' +\
                                    'The node degree is the number of edges connected to the node. ' +\
                                    'Connection weights are ignored in calculations.'

        description['in_degree'] = 'In directed graphs, the in-degree of a node is the number of ' +\
                                   'inward edges. Connection weights are ignored in calculations.'

        description['avg_in_degree'] = 'In directed graphs, the average in-degree is the average node '+\
                                       'in-degree. The node in-degree of a node is the number of ' +\
                                       'inward edges. Connection weights are ignored in calculations.'

        description['out_degree'] = 'In directed graphs, the out-degree of a node is the number of ' +\
                                    'outward edges. Connection weights are ignored in calculations.'

        description['avg_out_degree'] = 'In directed graphs, the average out-degree is the average ' +\
                                        'node out-degree. The node out-degree of a node is the number ' +\
                                        'of outward edges. Connection weights are ignored in calculations.'

        return description

    def compute_measure(graph):
        measure_dict = {}
        degree, in_degree, out_degree = MeasureDegree.degree(graph)
        if graph.is_directed():
            measure_dict['in_degree'] = in_degree
            measure_dict['out_degree'] = out_degree
            measure_dict['avg_in_degree'] = np.mean(in_degree)
            measure_dict['avg_out_degree'] = np.mean(out_degree)

        measure_dict['degree'] = degree
        measure_dict['avg_degree'] = np.mean(degree)
        return measure_dict

    def degree(graph):
        A = graph.A.copy()
        np.fill_diagonal(A, 0)

        if graph.is_weighted():
            A[A != 0] = 1

        in_degree = np.sum(A, 0)
        out_degree = np.sum(A, 1)
        degree = np.add(in_degree, out_degree)

        if graph.is_undirected():
            degree = np.multiply(degree, 0.5)

        return degree, in_degree, out_degree

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['degree', 'avg_degree']
        graph_type_measures[GraphBU] = ['degree', 'avg_degree']
        graph_type_measures[GraphWD] = ['degree', 'avg_degree']
        graph_type_measures[GraphWU] = ['degree', 'avg_degree']

        for graph_type in graph_type_measures.keys():
            if graph_type.get_setting('directed'):
                graph_type_measures[graph_type].extend(['in_degree', 'out_degree', 'avg_in_degree', 'avg_out_degree'])

        return graph_type_measures
