from braphy.graph.community_algorithms import CommunityAlgorithms
from braphy.graph.graph import Graph

class GraphWU(Graph):
    weighted = True
    directed = False
    def __init__(self, A, measure_list, rule_negative_weights = 'zero',
                 rule_symmetrize = 'max', rule_standardize = 'range'):
        A = Graph.remove_diagonal(A)
        A = Graph.remove_negative_weights(A, rule_negative_weights)
        A = Graph.standardize(A, rule_standardize)
        A = Graph.symmetrize(A, rule_symmetrize)
        super().__init__(A, measure_list)

    def is_selfconnected(self):
        return False

    def is_nonnegative(self):
        return True

    def get_name(self):
        return "Weighted Undirected Graph"

    def get_description(self):

        description = 'In a weighted undirected (WU) graph, ' + \
                      'the edges are associated with a real number ' + \
                      'between 0 and 1 ' + \
                      'indicating the strength of the connection, ' + \
                      'and they are undirected.' + \
                      'The connectivity matrix is symmetric.'

        return description

