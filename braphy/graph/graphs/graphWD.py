from braphy.graph.graphs import *
import numpy as np
import random
from braphy.utility.math_utility import (accumarray, divide_without_warning,
                                         multiply_without_warning)
import copy

class GraphWD(Graph):
    def __init__(self, A, settings):
        A = Graph.remove_diagonal(A)
        A = Graph.semipositivize(A, settings.rule_negative)
        A = Graph.standardize(A, settings.rule_standardize)
        super().__init__(A, settings)

    def match_settings():
        return {'weighted': True, 'directed': True}

    def get_name(self):
        return "Weighted Directed Graph"

    def get_description(self):

        description = 'In a weighted directed (WD) graph, ' + \
                'the edges are associated with a real number ' + \
                'between 0 and 1' + \
                'indicating the strength of the connection, ' + \
                'and they are directed.'

        return description

    def get_random_graph(self, attempts_per_edge = 5, number_of_weights = 1):
        W = self.A.copy()
        bd_settings = copy.deepcopy(self.settings)
        bd_settings.weighted = False
        graphBD = GraphBD(W, bd_settings)
        graphBD_random_A = graphBD.A
        W_bin = W>0
        N = np.size(graphBD_random_A,0) # number of nodes
        randomized_graph = np.zeros([N,N]) # initialize null model matrix

        S_in = sum(W) # nodal in-strength
        S_out = sum(W.T) # nodal out-strength
        W_sorted = np.sort(W[W_bin]) # sorted weights vector
        # find all the edges
        J_edges = np.where(graphBD_random_A.T)[0]
        I_edges = np.where(graphBD_random_A.T)[1]
        edges = I_edges + J_edges*N
        # expected weights matrix
        P = S_out[:,np.newaxis]*S_in[np.newaxis,:] # broadcasting

        for m in range(W_sorted.size,0,-number_of_weights):
            # sort the expected weights matrix
            ind = np.argsort(np.take(P.T,edges))

            # random index of sorted expected weight
            selected_indices = random.sample(range(0,m), min(m, number_of_weights))
            selected_edges = ind[selected_indices]

            # assign corresponding sorted weight at this index
            np.put(randomized_graph.T, edges[selected_edges],W_sorted[selected_indices])

            # recalculate expected weight for node I_edges[selected_edge]
            WAi = accumarray( I_edges[selected_edges], W_sorted[selected_indices], size=np.array([N, 1]))
            WAi=np.squeeze(WAi)
            Iu = WAi>0
            # readjust expected weight probabilities
            F = 1 - divide_without_warning(WAi[Iu],S_out[Iu])
            P[Iu,:] = multiply_without_warning(P[Iu,:],np.repeat(F[:,np.newaxis],N,axis=1))
            # readjust in-strength
            S_out[Iu] = S_out[Iu] - WAi[Iu]

            # recalculate expected weight for node J_edges[selected_edges]
            WAj = accumarray( J_edges[selected_edges], W_sorted[selected_indices], size=np.array([N, 1]))
            WAj=np.squeeze(WAj)
            Ju = WAj>0
            # readjust expected weight probabilities
            F = 1 - divide_without_warning(WAj[Ju],S_in[Ju])
            P[:,Ju] = multiply_without_warning(P[:,Ju],np.repeat(F[np.newaxis,:],N,axis=0))
            # readjust out-strength
            S_in[Ju] = S_in[Ju] - WAj[Ju]

            # remove the edge/weight from further consideration
            selected_edges = ind[selected_indices]
            edges = np.delete(edges, selected_edges)
            I_edges = np.delete(I_edges, selected_edges)
            J_edges = np.delete(J_edges, selected_edges)
            W_sorted = np.delete(W_sorted, selected_edges)

        rpos_in = np.corrcoef(sum(W, 0), sum(randomized_graph, 0))
        rpos_out = np.corrcoef(sum(W, 1), sum(randomized_graph, 1))
        correlation_coefficients = np.array([rpos_in.item(2), rpos_out.item(2)])

        return randomized_graph #, correlation_coefficients
