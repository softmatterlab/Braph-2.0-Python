import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_edge_betweenness_centrality import MeasureEdgeBetweennessCentrality
from braphy.test.test_utility import TestUtility
import numpy as np

class TestEdgeBetweennessCentrality(TestUtility):
    def test_wu(self):
        A = np.array([[0., 0.1, 0., 0., 0.],
                      [0.2, 0., 0., 0., 0.],
                      [0., 0., 0., 0.2, 0.],
                      [0., 0., 0.1, 0., 0.],
                      [0., 0., 0., 0., 0.,]])
        settings = GraphSettings(weighted = True, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        edge_betweenness_centrality = np.array([[0., 1, 0., 0., 0.],
                                                [1, 0., 0., 0., 0.],
                                                [0., 0., 0., 1, 0.],
                                                [0., 0., 1, 0., 0.],
                                                [0., 0., 0., 0., 0.,]])
        self.assertMatrixEqual(graph.get_measure(MeasureEdgeBetweennessCentrality, 'edge_betweenness_centrality').tolist(),
                                 edge_betweenness_centrality)

    def test_wd(self):
        A = np.array([[0., 0.1, 0.2, 0.3, 0.1],
                      [0.2, 0., 0., 0.9, 0.],
                      [0., 0.5, 0.0, 0.2, 0.],
                      [0., 0., 0., 0., 0.],
                      [1.0, 0.1, 0.1, 0.5, 0.,]])
        settings = GraphSettings(weighted = True, directed = True, rule_standardize = None)
        graph = GraphFactory.get_graph(A, settings)
        edge_betweenness_centrality = np.array([[0., 1, 1, 2, 4],
                                                [7, 0., 0., 0., 0.],
                                                [0., 3, 0., 2, 0.],
                                                [0., 0., 0, 0., 0.],
                                                [0., 2, 3, 0., 0.,]])
        self.assertMatrixEqual(graph.get_measure(MeasureEdgeBetweennessCentrality, 'edge_betweenness_centrality').tolist(),
                                 edge_betweenness_centrality)

    def test_bu(self):
        A = np.array([[0., 0.1, 0., 0., 0.],
                      [0.2, 0., 0., 0., 0.],
                      [0., 0., 0., 0.2, 0.],
                      [0., 0., 0.1, 0., 0.],
                      [0., 0., 0., 0., 0.,]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        edge_betweenness_centrality = np.array([[0., 1, 0., 0., 0.],
                                                [1, 0., 0., 0., 0.],
                                                [0., 0., 0., 1, 0.],
                                                [0., 0., 1, 0., 0.],
                                                [0., 0., 0., 0., 0.,]])
        self.assertMatrixEqual(graph.get_measure(MeasureEdgeBetweennessCentrality, 'edge_betweenness_centrality').tolist(),
                                 edge_betweenness_centrality)

    def test_bd(self):
        A = np.array([[0, 1, 1, 1, 1, 1],
                      [1, 0, 0, 0, 1, 0],
                      [1, 1, 0, 1, 1, 1],
                      [1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = False, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        edge_betweenness_centrality = np.array([[0, 1.5, 2, 2, 1.5, 2.5],
                                                [4, 0, 0, 0, 1, 0],
                                                [1, 1.5, 0, 1, 1.5, 1.5],
                                                [2.5, 0, 2.5, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0]])
        self.assertMatrixEqual(graph.get_measure(MeasureEdgeBetweennessCentrality, 'edge_betweenness_centrality').tolist(),
                                 edge_betweenness_centrality)

if __name__ == '__main__':
    unittest.main()
