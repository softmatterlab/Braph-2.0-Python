from braphy.graph.graphs.graph import Graph

class GraphWD(Graph):
    weighted = True
    directed = True
    def __init__(self,A, settings):
        A = Graph.remove_diagonal(A)
        A = Graph.semipositivize(A, settings.rule_semipositivize)
        A = Graph.standardize(A, settings.rule_standardize)
        super().__init__(A, settings)

    def is_undirected(self):
        return False

    def is_selfconnected(self):
        return False

    def is_nonnegative(self):
        return True

    def get_name(self):
        return "Weighted Directed Graph"

    def get_description(self):

        description = 'In a weighted directed (WD) graph, ' + \
                'the edges are associated with a real number ' + \
                'between 0 and 1' + \
                'indicating the strength of the connection, ' + \
                'and they are directed.'

        return description

    def get_random_graph(self, attempts_per_edge = 5):
        return None
