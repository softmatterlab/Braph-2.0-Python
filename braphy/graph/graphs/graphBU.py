from braphy.graph.graphs.graph import Graph

class GraphBU(Graph):
    weighted = False
    directed = False
    def __init__(self,A, settings):
        A = Graph.symmetrize(A, settings.rule_symmetrize)
        A = Graph.remove_diagonal(A)
        A = Graph.semipositivize(A, settings.rule_semipositivize)
        A = Graph.binarize(A)
        super().__init__(A, settings)

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

