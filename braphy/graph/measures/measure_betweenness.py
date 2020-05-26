from braphy.graph.measures.measure import Measure
from braphy.graph.graphs import *
import numpy as np
import copy

class MeasureBetweenness(Measure):

    def dimensions():
        d = {}
        d['betweenness'] = Measure.NODAL
        return d

    def get_description():

        description = {}
        description['betweenness'] = 'Node betweenness centrality of a node is the fraction of all ' +\
                      'shortest paths in the graph that contain a given node. ' + \
                      'Nodes with high values of betweenness centrality participate in ' + \
                      'a large number of shortest paths.'

        return description

    def compute_measure(graph, normalization = False):
        measure_dict = {}
        if graph.is_binary():
            betweenness = MeasureBetweenness.compute_binary_betweenness(graph)
        else:
            betweenness = MeasureBetweenness.compute_weighted_betweenness(graph)

        if normalization:
            N = np.size(graph.A[0])
            betweenness = betweenness/((N-1)*(N-2))

        measure_dict['betweenness'] = betweenness
        return measure_dict

    def compute_binary_betweenness(graph):
        A = graph.A.copy()
        N = np.size(A[0])
        d = 1
        NPd = A.copy()
        NSPd = NPd.copy()
        NSP = NSPd.copy()
        np.fill_diagonal(NSP, 1)
        L = NSP.copy()

        while(np.sum(NSPd)>0):
            d = d+1
            NPd = np.dot(NPd, A)
            NSPd = np.multiply(NPd, (L==0).astype(int))
            NSP = np.add(NSP, NSPd)
            L = np.add(L, np.multiply(d, (NSPd != 0).astype(int)))

        L = L.astype(float)
        L[L == 0] = np.inf
        np.fill_diagonal(L, 0)
        NSP[NSP == 0] = 1
        At = np.transpose(A)
        DP = np.zeros([N, N])
        diam = d;
        for d in range(diam, 2, -1):
            DPd1 = ((L==(d-1)).astype(int)*(1+DP)/NSP).dot(At) * ((L==(d-2)).astype(int) * NSP)
            DP = np.add(DP, DPd1)
        betweenness = np.sum(DP, axis = 0)
        return betweenness


    def compute_weighted_betweenness(graph):
        A = graph.A.copy()
        N = np.size(A[0])
        A[A!=0] = np.divide(1, A[A!=0]) 
        BC = np.zeros(N)

        for u in range(N):
            D = np.array([np.inf]*N)
            D[u] = 0
            NP = np.zeros(N)
            NP[u] = 1
            S = np.array([True]*N)
            P = np.zeros([N, N]).astype(bool)
            Q = np.zeros(N)
            q = N

            A1 = A.copy()
            V = [u]
            while True:
                S[V] = False
                A1[:,V] = 0
                for v in V:
                    Q[q-1] = v
                    q = q-1;
                    W = np.where(A1[v,:] > 0)[0]
                    for w in W:
                        Duw = D[v] + A1[v,w]
                        if Duw < D[w]:
                            D[w] = Duw
                            NP[w] = NP[v]
                            P[w,:] = 0
                            P[w, v] = 1
                        elif Duw == D.item(w):
                            NP[w] = NP.item(w) + NP.item(v)
                            P[w, v] = 1

                masked_D = D[S]
                if np.size(masked_D) == 0:
                    break

                minD = np.min(D[S])
                if minD == np.inf:
                    for i in range(q):
                        Q[i] = np.where(D == np.inf)[0][i]
                    break
                V = np.where(D == minD)[0]

            DP = np.zeros(N)
            Q = Q.astype(int)
            for w in Q[0:N-1]:
                BC[w] = BC[w] + DP[w]
                for v in np.where(P[w,:])[0]:
                    DP[v] = DP[v] + (1 + DP[w]) * NP[v] / NP[w]
        return BC.T

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['betweenness']
        graph_type_measures[GraphBU] = ['betweenness']
        graph_type_measures[GraphWD] = ['betweenness']
        graph_type_measures[GraphWU] = ['betweenness']

        return graph_type_measures
