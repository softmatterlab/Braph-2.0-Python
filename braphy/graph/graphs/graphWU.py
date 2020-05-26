from braphy.graph.graphs.graph import Graph

class GraphWU(Graph):
    weighted = True
    directed = False
    def __init__(self, A, settings):
        A = Graph.remove_diagonal(A)
        A = Graph.semipositivize(A, settings.rule_semipositivize)
        A = Graph.standardize(A, settings.rule_standardize)
        A = Graph.symmetrize(A, settings.rule_symmetrize)
        super().__init__(A, settings)

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

    def get_random_graph(self, attempts_per_edge = 5):
        return None
