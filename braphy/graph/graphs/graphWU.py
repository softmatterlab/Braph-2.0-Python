from braphy.graph.graphs import *
import numpy as np
import random
from braphy.utility.math_utility import (accumarray, divide_without_warning,
                                         multiply_without_warning)

class GraphWU(Graph):
    def __init__(self, A, settings):
        A = Graph.symmetrize(A, settings.rule_symmetrize)
        A = Graph.remove_diagonal(A)
        A = Graph.semipositivize(A, settings.rule_negative)
        A = Graph.standardize(A, settings.rule_standardize)
        
        super().__init__(A, settings)

    def match_settings():
        return {'weighted': True, 'directed': False}

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

    def get_random_graph(self, attempts_per_edge = 5, number_of_weights = 1):
        W = self.A.copy()
        graphBU = GraphBU(W,self.settings)
        graphBU_random_A = graphBU.get_random_graph()
        W_bin = W>0
        N = np.size(graphBU_random_A,0) # number of nodes
        randomized_graph = np.zeros([N,N]) # initialize null model matrix

        S = sum(W.T) # nodal strength
        W_sorted = np.sort(W[np.triu(W_bin)]) # sorted weights vector
        # find all the edges
        J_edges = np.where(np.triu(graphBU_random_A).T)[0]
        I_edges = np.where(np.triu(graphBU_random_A).T)[1]
        edges = I_edges + J_edges*N
        # expected weights matrix
        P = S[:,np.newaxis]*S[np.newaxis,:] # broadcasting

        for m in range(W_sorted.size,0,-number_of_weights):
            # sort the expected weights matrix
            ind = np.argsort(np.take(P.T,edges))

            # random index of sorted expected weight
            selected_indices = random.sample(range(0,m), min(m, number_of_weights))
            selected_edges = ind[selected_indices]

            # assign corresponding sorted weight at this index
            np.put(randomized_graph.T, edges[selected_edges],W_sorted[selected_indices])

            # recalculate expected weight for node I_edges[selected_edge]
            # cumulative weight
            WA = accumarray(np.concatenate((I_edges[selected_edges], J_edges[selected_edges]), axis=0), np.concatenate((W_sorted[selected_indices], W_sorted[selected_indices]), axis=0), size=np.array([N, 1]))
            WA=np.squeeze(WA)
            IJu = WA>0
            # readjust expected weight probabilities
            F = 1 - divide_without_warning(WA[IJu],S[IJu])
            P[IJu,:] = multiply_without_warning(P[IJu,:],np.repeat(F[:,np.newaxis],N,axis=1))
            P[:,IJu] = multiply_without_warning(P[:,IJu],np.repeat(F[np.newaxis,:],N,axis=0))
            # readjust strengths
            S[IJu] = S[IJu] - WA[IJu]

            # remove the edge/weight from further consideration
            selected_edges = ind[selected_indices]
            edges = np.delete(edges, selected_edges)
            I_edges = np.delete(I_edges, selected_edges)
            J_edges = np.delete(J_edges, selected_edges)
            W_sorted = np.delete(W_sorted, selected_edges)

        # calculate the final matrix
        randomized_graph = randomized_graph + randomized_graph.T

        rpos = np.corrcoef(sum(W), sum(randomized_graph))
        correlation_coefficients = np.array([rpos.item(2)])

        return randomized_graph #, correlation_coefficients
