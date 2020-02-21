from braphy.graph_measures.measure import Measure
from braphy.graph import *
import numpy as np
import copy

class MeasureGlobalEfficiency(Measure):

    def get_description():

        description = {}
        # PROOFREAD PLEASE 
        description['avg_global_efficiency'] = 'The global efficiency is the average inverse shortest path length ' +\
                                           'in the graph. It is inversely related to the characteristic path length.'

        description['global_efficiency'] = 'The global efficiency of a node is the average inverse shortest path ' +\
                                                'length of the node. It is inversely related to the path length of the node.'

        description['avg_in_global_efficiency'] = 'The characteristic in-global efficiency of a graph is the average of the ' +\
                                              'in-global efficiency of all nodes in the graph.'

        description['in_global_efficiency'] = 'The in-global efficiency of a node is the average inverse path length ' +\
                                                  'from the node itself to all other nodes.'

        description['avg_out_global_efficiency'] = 'The characteristic out-global efficiency of a graph is the average of the ' +\
                                               'out-global efficiency of all nodes in the graph.'

        description['out_global_efficiency'] = 'The out-global efficiency of a node is the average inverse path length ' +\
                                                   'from all other nodes to the node itself.'
        return description

    def compute_measure(graph):

        D = graph.D.copy()
        D_inverse = np.reciprocal(D)
        np.fill_diagonal(D_inverse, 0)

        in_global_efficiency = np.sum(D_inverse, axis = 0)/(len(D) - 1)
        out_global_efficiency = np.sum(D_inverse, axis = 1)/(len(D) - 1)
        global_efficiency = (in_global_efficiency + out_global_efficiency) / 2

        graph.measure_dict[MeasureGlobalEfficiency]['global_efficiency'] = global_efficiency
        graph.measure_dict[MeasureGlobalEfficiency]['avg_global_efficiency'] = np.mean(global_efficiency)
        if graph.is_directed():
            graph.measure_dict[MeasureGlobalEfficiency]['in_global_efficiency'] = in_global_efficiency
            graph.measure_dict[MeasureGlobalEfficiency]['avg_in_global_efficiency'] = np.mean(in_global_efficiency)
            graph.measure_dict[MeasureGlobalEfficiency]['out_global_efficiency'] = out_global_efficiency
            graph.measure_dict[MeasureGlobalEfficiency]['avg_out_global_efficiency'] = np.mean(out_global_efficiency)

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['global_efficiency', 'avg_global_efficiency']
        graph_type_measures[GraphBU] = ['global_efficiency', 'avg_global_efficiency']
        graph_type_measures[GraphWD] = ['global_efficiency', 'avg_global_efficiency']
        graph_type_measures[GraphWU] = ['global_efficiency', 'avg_global_efficiency']

        for graph_type in graph_type_measures.keys():
            if graph_type.directed:
                graph_type_measures[graph_type].extend(['in_global_efficiency',
                                                        'avg_in_global_efficiency',
                                                        'out_global_efficiency',
                                                        'avg_out_global_efficiency'])

        return graph_type_measures