from braphy.graph.graphs.graph import Graph
import numpy as np
import random

class GraphBU(Graph):
    def __init__(self, A, settings):
        A = Graph.symmetrize(A, settings.rule_symmetrize)
        A = Graph.remove_diagonal(A)
        A = Graph.semipositivize(A, settings.rule_negative)
        A = Graph.binarize(A, settings.rule_binary, settings.value_binary)
        super().__init__(A, settings)

    def match_settings():
        return {'weighted': False, 'directed': False}

    def get_name(self):
        return "Binary Undirected Graph"

    def get_description(self):
        description = 'In a binary undirected (BU) graph, ' + \
                      'the edges can be either 0 (absence of connection) ' + \
                      'or 1 (existence of connection), ' + \
                      'and they are undirected.' + \
                      'The connectivity matrix is symmetric.'
        return description

    def get_random_graph(self, attempts_per_edge = 5, number_of_weights = None):
        J_edges = np.where(np.triu(self.A).T)[0]
        I_edges = np.where(np.triu(self.A).T)[1]
        E = len(I_edges)

        randomized_graph = self.A.copy()
        swaps = 0

        for attempt in range(0, (attempts_per_edge*E)):
            #select two edges
            selected_edges = random.sample(range(0, E), 2)
            node_start_1 = I_edges[selected_edges[0]]
            node_end_1 = J_edges[selected_edges[0]]
            node_start_2 = I_edges[selected_edges[1]]
            node_end_2 = J_edges[selected_edges[1]]

            if random.uniform(0, 1) > 0.5:
                I_edges[selected_edges[1]] = node_end_2
                J_edges[selected_edges[1]] = node_start_2

                node_start_2 = I_edges[selected_edges[1]]
                node_end_2 = J_edges[selected_edges[1]]

            # Swap edges if:
            # 1) no edge between node_start_2 and node_end_1
            # 2) no edge between node_start_1 and node_end_2
            # 3) node_start_1 ~= node_start_2
            # 4) node_end_1 ~= node_end_2
            # 5) node_start_1 ~= node_end_2
            # 6) node_start_2 ~= node_end_1
            if (not randomized_graph[node_start_1, node_end_2] and 
                not randomized_graph[node_start_2, node_end_1] and 
                node_start_1 != node_start_2 and node_end_1 != node_end_2 and 
                node_start_1 != node_end_2 and node_start_2 != node_end_1):

                # erase old edges 
                randomized_graph[node_start_1, node_end_1] = 0
                randomized_graph[node_end_1, node_start_1] = 0

                randomized_graph[node_start_2, node_end_2] = 0
                randomized_graph[node_end_2, node_start_2] = 0

                # write new edges 
                randomized_graph[node_start_1, node_end_2] = 1
                randomized_graph[node_end_2, node_start_1] = 1

                randomized_graph[node_start_2, node_end_1] = 1
                randomized_graph[node_end_1, node_start_2] = 1

                # update edge list 
                J_edges[selected_edges[0]] = node_end_2
                J_edges[selected_edges[1]] = node_end_1

                swaps = swaps+1

        return randomized_graph #, swaps
