from braphy.graph_measures import *
import numpy as np
from braphy.graph import *
import copy
from braphy.graph_measures.measure_path_length import MeasurePathLength




class MeasureCloseness(Measure):

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
        
        if graph.is_directed():
            
            graph.measure_dict[MeasureCloseness]['closeness_in'] = \
                                1./graph.get_measure(MeasurePathLength, 'in_path_length')
            
            graph.measure_dict[MeasureCloseness]['closeness_out'] = \
                                1./graph.get_measure(MeasurePathLength,'out_path_length')

        graph.measure_dict[MeasureCloseness]['closeness'] = \
                                1./graph.get_measure(MeasurePathLength,'path_length')

    def get_valid_graph_types():
        graph_type_measures = {}
        undirected_list = ['closeness']
        directed_list = ['closeness', 'closeness_in', 'closeness_out']
        graph_type_measures[GraphBD] = directed_list
        graph_type_measures[GraphBU] = undirected_list
        graph_type_measures[GraphWD] = directed_list
        graph_type_measures[GraphWU] = undirected_list

        return graph_type_measures

    '''
    def pl(self, g:):

    PL path length of node
    [C,CIN,COUT] = PL(G) calculates the path length C, in-path length CIN
    and out-path length COUT of all nodes in the graph G.
    
    The path length is the average shortest path lengths of one node to all
    other nodes. The path length of a node is the average of the in-path
    and out-path length of that node.
    
    Reference: "Complex network measures of brain connectivity: Uses and
                iterpretations", M. Rubinov, O. Sporns

    See also Graph, distance.
    '''


