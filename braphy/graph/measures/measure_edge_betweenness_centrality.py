from braphy.graph.measures.measure import Measure
from braphy.graph.graphs import *
import numpy as np

class MeasureEdgeBetweennessCentrality(Measure):

    def get_description():
        description = {}
        description['edge_betweenness_centrality'] = 'The fraction of all shortest paths in the graph that ' \
                                                     'pass through a given edge. Edgets with high values of ' \
                                                     'betweenness centrality participate in a large number ' \
                                                     'of shortest paths.'
        return description

    def compute_measure(graph):
        A = graph.A.copy()
        n = len(A)

        BC = np.zeros(n)
        EBC = np.zeros([n, n])

        if graph.is_binary():
            for u in range(n):
                D = np.zeros(n).astype(bool) # Distance from u
                D[u] = True
                NP = np.zeros(n) # Number of paths from u
                NP[u] = 1
                P = np.zeros([n, n]).astype(bool) # Predecessors
                Q = np.zeros(n) # Order of non-increasing distance
                q = n
                Gu = A.copy()
                V = [u]
                while len(V)>0:
                    Gu[:, V] = 0 # Remove remaining in-edges
                    for v in V:
                        Q[q-1] = v
                        q -= 1
                        W = np.where(Gu[v, :] > 0)[0] # Neighbours of v
                        for w in W:
                            if D[w]:
                                NP[w] = NP[w] + NP[v] # NP[u->w] sum of old and new
                                P[w, v] = 1 # v is a predecessor
                            else:
                                D[w] = True
                                NP[w] = NP[v]
                                P[w, v] = 1
                    V = np.where(np.any(Gu[V, :], 0))[0]
                if not np.all(D): # if some vertices are unreachable,
                    where = np.where(D == 0)[0]
                    for i in range(q): # ... these are first-in-line
                        Q[i] = where[i]
                DP = np.zeros(n) # Dependency
                Q = Q.astype(int)
                for w in Q[:n-1]:
                    BC[w] = BC[w] + DP[w]
                    for v in np.where(P[w,:])[0]:
                        DPvw = (1 + DP[w])*NP[v]/NP[w]
                        DP[v] = DP[v] + DPvw
                        EBC[v, w] = EBC[v, w] + DPvw

            edge_betweenness_centrality = EBC

        elif graph.is_weighted():
            for u in range(n):
                D = np.array([np.inf]*n) # Distance from u
                D[u] = 0
                NP = np.zeros(n) # Number of paths from u
                NP[u] = 1
                S = np.ones(n).astype(bool) # Distance permanence (true is temporary)
                P = np.zeros([n, n]).astype(bool) # Predecessors
                Q = np.zeros(n) # Order of non-increasing distance
                q = n
                G1 = A.copy()
                V = [u]
                while True:
                    S[V] = 0 # Distance u->V is now permanent
                    G1[:, V] = 0 # No in-edges as already shortest
                    for v in V:
                        Q[q-1] = v
                        q -= 1
                        W = np.where(G1[v, :] > 0)[0] # Neighbours of v
                        for w in W:
                            Duw = D[v] + G1[v, w] # Path length to be tested
                            if Duw < D[w]: # if new u->w shorter than old
                                D[w] = Duw
                                NP[w] = NP[v] # NP[u->w] = NP of new path
                                P[w, :] = 0
                                P[w, v] = 1 # v is the only predecessor
                            elif Duw == D[w]: # if new u-> equal to old
                                NP[w] = NP[w] + NP[v] # NP[u->w] sum of old and new
                                P[w, v] = 1 # v is also a predecessor
                    if np.size(D[S]) == 0:
                        break
                    minD = np.min(D[S])
                    if minD == np.inf:
                        where = np.where(D == np.inf)[0]
                        for i in range(q):
                            Q[i] = where[i]
                        break
                    V = np.where(D == minD)[0]

                DP = np.zeros(n) # Dependency
                Q = Q.astype(int)
                for w in Q[:n-1]:
                    BC[w] = BC[w] + DP[w]
                    for v in np.where(P[w,:])[0]:
                        DPvw = (1 + DP[w])*NP[v]/NP[w]
                        DP[v] = DP[v] + DPvw
                        EBC[v, w] = EBC[v, w] + DPvw

            edge_betweenness_centrality = EBC

        measure_dict = {'edge_betweenness_centrality': edge_betweenness_centrality}
        return measure_dict


    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['edge_betweenness_centrality']
        graph_type_measures[GraphBU] = ['edge_betweenness_centrality']
        graph_type_measures[GraphWD] = ['edge_betweenness_centrality']
        graph_type_measures[GraphWU] = ['edge_betweenness_centrality']

        return graph_type_measures
