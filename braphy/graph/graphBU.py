from braphy.graph.graph import Graph
from braphy.graph.community_algorithms import CommunityAlgorithms

class GraphBU(Graph):
    weighted = False
    directed = False
    def __init__(self,A, measure_list, rule_negative_weights = 'zero', rule_symmetrize = 'max'):
        A = Graph.symmetrize(A, rule_symmetrize)
        A = Graph.remove_diagonal(A)
        A = Graph.remove_negative_weights(A, rule_negative_weights)
        A = Graph.binarize(A)
        
        super().__init__(A, measure_list)

    def is_selfconnected(self):
        return False

    def is_nonnegative(self):
        return True

    def get_name(self):
        return "Binary Undirected Graph"

    def get_description(self):
        
        description = 'In a binary undirected (BU) graph, ' + \
                      'the edges can be either 0 (absence of connection) ' + \
                      'or 1 (existence of connection), ' + \
                      'and they are undirected.' + \
                      'The connectivity matrix is symmetric.'
        
        return description
