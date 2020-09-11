from braphy.graph.measures.measure import Measure
from braphy.graph.measures.measure_distance import MeasureDistance
from braphy.graph.graphs import *
from braphy.utility.math_utility import divide_without_warning
import numpy as np
import copy

class MeasureGlobalEfficiency(Measure):
    def dimensions():
        d = {}
        d['global_efficiency'] = Measure.NODAL
        d['avg_global_efficiency'] = Measure.GLOBAL
        d['in_global_efficiency'] = Measure.NODAL
        d['avg_in_global_efficiency'] = Measure.GLOBAL
        d['out_global_efficiency'] = Measure.NODAL
        d['avg_out_global_efficiency'] = Measure.GLOBAL
        return d

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
        measure_dict = {}
        D = graph.get_measure(MeasureDistance, 'distance').copy()
        D_inverse = divide_without_warning(1, D)
        np.fill_diagonal(D_inverse, 0)

        in_global_efficiency = np.sum(D_inverse, axis = 0)/(len(D) - 1)
        out_global_efficiency = np.sum(D_inverse, axis = 1)/(len(D) - 1)
        global_efficiency = (in_global_efficiency + out_global_efficiency) / 2

        if graph.is_directed():
            measure_dict['in_global_efficiency'] = in_global_efficiency
            measure_dict['avg_in_global_efficiency'] = np.mean(in_global_efficiency)
            measure_dict['out_global_efficiency'] = out_global_efficiency
            measure_dict['avg_out_global_efficiency'] = np.mean(out_global_efficiency)
        else:
            measure_dict['global_efficiency'] = global_efficiency
            measure_dict['avg_global_efficiency'] = np.mean(global_efficiency)

        return measure_dict

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['in_global_efficiency', 'avg_in_global_efficiency',
                                        'out_global_efficiency', 'avg_out_global_efficiency']
        graph_type_measures[GraphBU] = ['global_efficiency', 'avg_global_efficiency']
        graph_type_measures[GraphWD] = ['in_global_efficiency', 'avg_in_global_efficiency',
                                        'out_global_efficiency', 'avg_out_global_efficiency']
        graph_type_measures[GraphWU] = ['global_efficiency', 'avg_global_efficiency']

        for graph_type in graph_type_measures.keys():
            if graph_type.get_setting('directed'):
                graph_type_measures[graph_type].extend(['in_global_efficiency',
                                                        'avg_in_global_efficiency',
                                                        'out_global_efficiency',
                                                        'avg_out_global_efficiency'])

        return graph_type_measures
