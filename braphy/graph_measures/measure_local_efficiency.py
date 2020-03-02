from braphy.graph_measures.measure import Measure
from braphy.graph_measures.measure_distance import MeasureDistance
from braphy.graph import *
from braphy.utility.helper_functions import divide_without_warning
import numpy as np
import copy

class MeasureLocalEfficiency(Measure):

    def get_description():
        description = {}
        description['local_efficiency'] = 'The local efficiency of a node is the global efficiency ' +\
                                          'of the node computed on the node''s neighborhood'
        description['avg_local_efficiency'] = 'The local efficiency of a graph is the average of '+\
                                              'the local efficiencies of its nodes. It is related to clustering coefficient.'

        return description

    def compute_measure(graph):

        A = graph.A.copy()
        local_efficiency = np.zeros(len(A))

        for i in range(len(A)):
            neighbours = np.where(A[i,:] + A[:,i])[0]
            if len(neighbours) > 1:
                if graph.is_binary():
                    A_subgraph = A[neighbours,:][:,neighbours]
                else:
                    A_subgraph = A[neighbours,:][:,neighbours] * np.sqrt(np.dot(A[i,neighbours], A[neighbours,i]))

                D_subgraph = MeasureDistance.distance(A_subgraph, graph.is_weighted(), graph.is_directed())
                D_subgraph_inverse = divide_without_warning(1, D_subgraph)
                np.fill_diagonal(D_subgraph_inverse, 0)

                in_local_efficiency = np.sum(D_subgraph_inverse, axis = 0)/(len(D_subgraph) - 1)
                out_local_efficiency = np.sum(D_subgraph_inverse, axis = 1)/(len(D_subgraph) - 1)
                local_efficiency[i] = np.mean((in_local_efficiency + out_local_efficiency) / 2)

        graph.measure_dict[MeasureLocalEfficiency]['local_efficiency'] = local_efficiency
        graph.measure_dict[MeasureLocalEfficiency]['avg_local_efficiency'] = np.mean(local_efficiency)

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['local_efficiency', 'avg_local_efficiency']
        graph_type_measures[GraphBU] = ['local_efficiency', 'avg_local_efficiency']
        graph_type_measures[GraphWD] = ['local_efficiency', 'avg_local_efficiency']
        graph_type_measures[GraphWU] = ['local_efficiency', 'avg_local_efficiency']

        return graph_type_measures
