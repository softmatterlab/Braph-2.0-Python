from braphy.graph_measures.measure import Measure
from braphy.graph_measures.measure_distance import MeasureDistance
from braphy.graph import *
import numpy as np
import copy

class MeasurePathLength(Measure):

    def get_description():
        description = {}
        description['path_length'] = 'For undirected graphs, the path length of a node is ' +\
                                     'the average path length from the note to all other nodes. ' +\
                                     'For directed graphs, it is the sum of the in-path length and of the out-path length.'
        description['char_path_length'] = 'The characteristic path length of a graph is the average ' +\
                                          'shortest path length in the graph. It is the average of ' +\
                                          'the path length of all nodes in the graph.'
        description['in_path_length'] = 'The in-path length of a node is the average path length from ' +\
                                        'the node itself to all other nodes.'

        description['out_path_length'] = 'The out-path length of a node is the average path length from ' +\
                                         'all other nodes to the node itself.'

        description['char_in_path_length'] = 'The characteristic in-path length of a graph is the average of ' +\
                                             'the in-path length of all nodes in the graph.'

        description['char_out_path_length'] = 'The characteristic out-path length of a graph is the average of ' +\
                                              'the out-path length of all nodes in the graph.'
        return description

    def compute_measure(graph):
        D = graph.get_measure(MeasureDistance, 'distance').copy()
        np.fill_diagonal(D, 0)
        nbr_nodes = len(D)

        infinite_distances = (D == np.inf).astype(float)
        D[D == np.inf] = 0

        in_path_length = np.zeros(len(D))
        out_path_length = np.zeros(len(D))
        for i in range(len(D)):
            nbr_of_paths_to_avg_in = nbr_nodes - 1 - np.sum(infinite_distances, axis = 0)[i]
            nbr_of_paths_to_avg_out = nbr_nodes - 1 - np.sum(infinite_distances, axis = 1)[i]
            if nbr_of_paths_to_avg_in <= 0:
                in_path_length[i] = np.nan
            else:
                in_path_length[i] = np.sum(D[:,i]) / nbr_of_paths_to_avg_in
            if nbr_of_paths_to_avg_out <= 0:
                out_path_length[i] = np.nan
            else:
                out_path_length[i] = np.sum(D[i,:]) / nbr_of_paths_to_avg_out
        path_length = (in_path_length + out_path_length) / 2

        graph.measure_dict[MeasurePathLength]['path_length'] = path_length
        graph.measure_dict[MeasurePathLength]['char_path_length'] = np.nanmean(path_length)
        if graph.is_directed():
            graph.measure_dict[MeasurePathLength]['in_path_length'] = in_path_length
            graph.measure_dict[MeasurePathLength]['out_path_length'] = out_path_length
            graph.measure_dict[MeasurePathLength]['char_in_path_length'] = np.nanmean(in_path_length)
            graph.measure_dict[MeasurePathLength]['char_out_path_length'] = np.nanmean(out_path_length)

    def get_valid_graph_types():

        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['path_length', 'char_path_length']
        graph_type_measures[GraphBU] = ['path_length', 'char_path_length']
        graph_type_measures[GraphWD] = ['path_length', 'char_path_length']
        graph_type_measures[GraphWU] = ['path_length', 'char_path_length']

        for graph_type in graph_type_measures.keys():
            if graph_type.directed:
                graph_type_measures[graph_type].extend(['in_path_length', 'char_in_path_length',
                                                        'out_path_length', 'char_out_path_length'])

        return graph_type_measures
