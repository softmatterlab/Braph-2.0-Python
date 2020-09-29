from braphy.graph.measures.measure import Measure
from braphy.graph.measures.measure_distance import MeasureDistance
from braphy.graph.graphs import *
from braphy.utility.math_utility import divide_without_warning
import numpy as np
import copy

class MeasureLocalEfficiency(Measure):
    def dimensions():
        d = {}
        d['local_efficiency'] = Measure.NODAL
        d['in_local_efficiency'] = Measure.NODAL
        d['out_local_efficiency'] = Measure.NODAL
        d['avg_local_efficiency'] = Measure.GLOBAL
        d['avg_in_local_efficiency'] = Measure.GLOBAL
        d['avg_out_local_efficiency'] = Measure.GLOBAL
        return d

    def get_description():
        description = {}
        description['local_efficiency'] = 'The local efficiency of a node is the global efficiency ' +\
                                          'of the node computed on the node''s neighborhood'
        description['avg_local_efficiency'] = 'The average local efficiency of a graph is the average of '+\
                                              'the local efficiencies of its nodes. It is related to clustering coefficient.'
        description['in_local_efficiency'] = 'The in-local efficiency of a node is the in-global efficiency ' +\
                                             'of the node computed on the node''s neighborhood'
        description['out_local_efficiency'] = 'The out-local efficiency of a node is the out-global efficiency ' +\
                                             'of the node computed on the node''s neighborhood'
        description['avg_in_local_efficiency'] = 'The average in-local efficiency of a graph is the average of '+\
                                              'the in-local efficiencies of its nodes. It is related to clustering coefficient.'
        description['avg_out_local_efficiency'] = 'The average out-local efficiency of a graph is the average of '+\
                                              'the out-local efficiencies of its nodes. It is related to clustering coefficient.'

        return description

    def compute_measure(graph):
        measure_dict = {}
        A = graph.A.copy()
        local_efficiency = np.zeros(len(A))
        in_local_efficiency = np.zeros(len(A))
        out_local_efficiency = np.zeros(len(A))

        for i in range(len(A)):
            neighbours = np.where(A[i,:] + A[:,i])[0]
            if len(neighbours) > 1:
                A_subgraph = A[neighbours,:][:,neighbours]
                D_subgraph = MeasureDistance.distance(A_subgraph, graph.is_weighted(), graph.is_directed())['distance']
                D_subgraph_inverse = divide_without_warning(1, D_subgraph)
                np.fill_diagonal(D_subgraph_inverse, 0)

                if not graph.is_directed():
                    global_efficiency_D = np.sum(D_subgraph_inverse, axis = 0)/(len(D_subgraph) - 1)
                    local_efficiency[i] = np.mean(global_efficiency_D)

                in_local_efficiency_i = np.sum(D_subgraph_inverse, axis = 0)/(len(D_subgraph) - 1)
                out_local_efficiency_i = np.sum(D_subgraph_inverse, axis = 1)/(len(D_subgraph) - 1)

                in_local_efficiency[i] = np.mean(in_local_efficiency_i)
                out_local_efficiency[i] = np.mean(out_local_efficiency_i)

        if graph.is_directed():
            measure_dict['in_local_efficiency'] = in_local_efficiency
            measure_dict['avg_in_local_efficiency'] = np.mean(in_local_efficiency)
            measure_dict['out_local_efficiency'] = out_local_efficiency
            measure_dict['avg_out_local_efficiency'] = np.mean(out_local_efficiency)
        else:
            measure_dict['local_efficiency'] = local_efficiency
            measure_dict['avg_local_efficiency'] = np.mean(local_efficiency)
        return measure_dict

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['in_local_efficiency', 'avg_in_local_efficiency',
                                        'out_local_efficiency', 'avg_out_local_efficiency']
        graph_type_measures[GraphBU] = ['local_efficiency', 'avg_local_efficiency']
        graph_type_measures[GraphWD] = ['in_local_efficiency', 'avg_in_local_efficiency',
                                        'out_local_efficiency', 'avg_out_local_efficiency']
        graph_type_measures[GraphWU] = ['local_efficiency', 'avg_local_efficiency']

        return graph_type_measures
