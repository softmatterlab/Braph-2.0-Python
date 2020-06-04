from braphy.graph.measures.measure import Measure
from braphy.graph.graphs import *
import numpy as np
import copy

class MeasurePathTransitivity(Measure):

    def get_description():
        description = {}
        description['path_transitivity'] = 'The path transitivity provides the density of ' +\
                                           'triangles that are available along the shortest-paths ' +\
                                           'between pairs of nodes.'
        return description

    def compute_measure(graph):
        measure_dict = {}
        A = graph.A.copy()

        if graph.is_binary() and graph.is_undirected():
            N = np.size(A[0])
            m = np.zeros([N,N]) #matching index
            path_transitivity = np.zeros([N,N])

            for i in range(0,(N-1)):
                for j in range((i+1), N):
                    x = 0
                    y = 0
                    z = 0
                    for k in range(0,N):
                        if A[i,k] and A[j,k] and k!=i and k!=j:
                            x += A[i,k] + A[j,k]
                        if k!=j:
                            y += A[i,k]
                        if k!=i:
                            z += A[j,k]
                    m[i,j] = x/(y+z)

            m = m + np.transpose(m)

            '''
            Calculate hops and Pmat:
            SPL = Unweighted/weighted shortest path length matrix
            hops = number of edges in the shortest path matrix
            Pmat = elements {i,j} in this matrix indicate the next node in the shortest path
            between i and j 
            '''

            SPL = A.copy()
            SPL = SPL.astype(float)
            SPL[SPL == 0] = np.inf
            hops = (A!=0).astype(float)
            Pmat = np.tile(np.arange(1,N+1), (N,1))

            for k in range(0,N):
                i2k_k2j = SPL[np.newaxis,:,k]+SPL[k,:,np.newaxis] #broadcasting
                path = SPL > i2k_k2j
                indices = np.argwhere(path==1)
                [j,i] = np.hsplit(indices, 2)
                values_to_place = hops[i,k] + hops[k,j]
                flat_indices = np.ravel_multi_index([j,i],path.shape)
                np.put(hops,flat_indices,values_to_place)
                np.put(Pmat,flat_indices,Pmat[i,k])
                SPL = np.minimum(SPL, i2k_k2j)

            np.fill_diagonal(hops, 0)
            np.fill_diagonal(Pmat, 0)

            # Calculate path transitivity
            for i in range(0,N-1):
                for j in range(i+1,N):
                    x = 0
                    # Retrieve shortest path
                    s = i
                    t = j
                    path_length = hops[s,t]

                    if path_length:
                        path = np.empty([int(path_length)+1,1])
                        path[:] = np.nan
                        path[0] = s
                        for ind in range(1,len(path)):
                            s = Pmat[s,j]
                            path[ind] = t
                    else:
                        path = []
                    # Calculate triangles on path
                    K = len(path)
                    for t in range(0,K-1):
                        for l in range(t+1, K):
                            x = x + m[int(path[t]), int(path[l])]

                    path_transitivity[i,j] = 2*x/(K*(K-1))

            path_transitivity = path_transitivity + path_transitivity.T
            path_transitivity[np.isnan(path_transitivity)] = 0

        measure_dict['path_transitivity'] = path_transitivity
        return measure_dict

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBU] = ['path_transitivity']

        return graph_type_measures