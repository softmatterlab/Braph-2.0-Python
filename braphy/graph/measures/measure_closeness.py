from braphy.graph.measures import *
import numpy as np
from braphy.graph.graphs import *
import copy
from braphy.graph.measures.measure_path_length import MeasurePathLength

class MeasureCloseness(Measure):

    def dimensions():
        d = {}
        d['closeness'] = Measure.NODAL
        d['closeness_in'] = Measure.NODAL
        d['closeness_out'] = Measure.NODAL
        return d

    def get_description():

        description = {}

        # Proofread please
        description['closeness'] = 'The closeness centrality of a node is the inverse of the average ' +\
                      'shortest path length from the node to all other nodes in the graph.'

        description['closeness_in'] = 'The in-closeness centrality of a node is the inverse of the average ' +\
                      'shortest path length from the node to all other nodes in the graph.'

        description['closeness_out'] = 'The out-closeness centrality of a node is the inverse of the average ' +\
                      'shortest path length from all other nodes in the graph to the node.'

        return description

    def compute_measure(graph):
        measure_dict = {}
        if graph.is_directed():
            measure_dict['closeness_in'] = 1/graph.get_measure(MeasurePathLength,
                                                               'in_path_length', save = False)
            measure_dict['closeness_out'] = 1/graph.get_measure(MeasurePathLength,
                                                                'out_path_length', save = False)
        else:
            measure_dict['closeness'] = 1/graph.get_measure(MeasurePathLength,'path_length', save = False)
        return measure_dict

    def get_valid_graph_types():
        graph_type_measures = {}
        undirected_list = ['closeness']
        directed_list = ['closeness_in', 'closeness_out']
        graph_type_measures[GraphBD] = directed_list
        graph_type_measures[GraphBU] = undirected_list
        graph_type_measures[GraphWD] = directed_list
        graph_type_measures[GraphWU] = undirected_list

        return graph_type_measures

