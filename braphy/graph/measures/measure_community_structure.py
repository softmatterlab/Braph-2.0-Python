from braphy.graph.measures.measure import Measure
import numpy as np
from braphy.graph.graphs import *
import copy

class MeasureCommunityStructure(Measure):

    def dimensions():
        d = {}
        d['community_structure'] = Measure.NODAL
        d['modularity'] = Measure.NODAL
        return d

    def get_description():
        description = {}
        description['community_structure'] = 'cs'
        description['modularity'] = 'm'
        return description

    def compute_measure(graph):
        measure_dict = {}
        community_structure, modularity = MeasureCommunityStructure.compute_community(graph.A,
                                          graph.is_weighted(), graph.is_directed())
        measure_dict['community_structure'] = community_structure
        measure_dict['modularity'] = modularity
        return measure_dict

    def compute_community(A, is_weighted, is_directed, algorithm = 'Louvain', gamma = 1):
        algorithms = {'Louvain':CommunityAlgorithms.louvain_iterations,
                      'Fixed':CommunityAlgorithms.fixed}
        assert algorithm in algorithms.keys()
        return algorithms[algorithm](A, is_weighted, is_directed, gamma)

    def louvain_iterations(A, is_weighted, is_directed, gamma):
        M, Q = CommunityAlgorithms.louvain(A, is_weighted, is_directed, gamma)
        for _ in range(2):
            _M, _Q = CommunityAlgorithms.louvain(A, is_weighted, is_directed,
                                                 gamma)
            if(_Q > Q):
                M = _M
                Q = _Q
        return M, Q

    def louvain(A, is_weighted, is_directed, gamma):
        A = A.copy()
        N = np.size(A, 0)
        s = np.sum(A)
        A[A < 0] = 0
        assert np.min(A) >= 0
        M0 = np.array(list(range(N)))
        Mb = np.unique(M0, return_inverse = True)[1]
        M = Mb.copy();
        B = 'modularity'
        if (B == 'modularity'):
            B = A-gamma*(np.outer(np.sum(A, 1),(np.sum(A, 0))))/s

        B = (B+B.T)/2
        Hnm = np.zeros([N, N])
        for m in range(np.max(Mb)+1):
            Hnm[:, m] = np.sum(B[:, np.where(Mb==m)[0]],1)

        H = np.sum(Hnm, 1)
        Hm = np.sum(Hnm, 0)
        Q0 = -np.inf
        Q = np.trace(B)/s
        first = True
        while Q-Q0 > 1e-10:
            flag = True
            while flag:
                flag = False
                for u in np.random.permutation(N):
                    ma = Mb[u]
                    dQ = Hnm[u,:] - Hnm[u,ma] + B[u,u]
                    dQ[ma] = 0
                    mb = np.argmax(dQ)
                    max_dQ = dQ[mb]
                    if max_dQ > 1e-10:
                        flag = True
                        Mb[u] = mb
                        Hnm[:, mb] = Hnm[:, mb] + B[:, u]
                        Hnm[:, ma] = Hnm[:, ma] - B[:, u]
                        Hm[mb] = Hm[mb] + H[u]
                        Hm[ma] = Hm[ma] - H[u]
            Mb = np.unique(Mb, return_inverse = True)[1]
            M0 = M.copy()
            if first:
                M = Mb.copy()
                first = False
            else:
                for u in range(N):
                    M[M0 == u] = Mb[u]
            if (np.size(Mb)==0):
                N = np.array([])
            else:
                N = np.max(Mb) + 1
            B1 = np.zeros([N, N])
            for u in range(N):
                for v in range(u, N):
                    bm = np.sum(B[np.where(Mb==u)[0],:][:,np.where(Mb==v)[0]])
                    B1[u, v] = bm
                    B1[v, u] = bm
            B = B1.copy()
            Mb = np.array(list(range(N)))
            Hnm = B.copy()
            H = np.sum(B, 0)
            Hm = H.copy()
            Q0 = Q.copy()
            Q = np.trace(B)/s
        return M.T, Q

    def fixed(A, is_weighted, is_directed, gamma):
        N = np.size(A, 0)
        Ci = np.ones(N)
        Q = 0;
        return Ci, Q

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['community_structure', 'modularity']
        graph_type_measures[GraphBU] = ['community_structure', 'modularity']
        graph_type_measures[GraphWD] = ['community_structure', 'modularity']
        graph_type_measures[GraphWU] = ['community_structure', 'modularity']

        return graph_type_measures

    def community_dependent():
        return True
