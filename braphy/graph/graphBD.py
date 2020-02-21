from braphy.graph.community_algorithms import CommunityAlgorithms
from braphy.graph.graph import Graph
import numpy as np

class GraphBD(Graph):
    weighted = False
    directed = True
    def __init__(self, A, measure_list, rule_negative_weights = 'zero'):
        A = Graph.remove_diagonal(A)
        A = Graph.remove_negative_weights(A, rule_negative_weights)
        super().__init__(A, measure_list)

    def is_selfconnected(self):
        return False

    def is_nonnegative(self):
        return True

    def get_name(self):
        return "Binary Directed Graph"

    def get_description(self):
        
        description = 'In a binary directed (BD) graph, ' + \
                      'the edges can be either 0 (absence of connection) ' + \
                      'or 1 (existence of connection), ' + \
                      'and they are directed.' 

        return description
