import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_triangles import MeasureTriangles
from braphy.test.test_utility import TestUtility
import numpy as np

class TestTriangles(TestUtility):
    def test_graphBD(self):
        A = np.array([[0,0,1,0],
                      [1,0,0,1],
                      [0,1,0,1],
                      [0,0,0,0]])
        settings = GraphSettings(weighted = False, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceEqual(graph.get_measure(MeasureTriangles, 'triangles').tolist(),
                                 [1, 1, 1, 0])

    def test_graphBU(self):
        A = np.array([[0,0,1,0,0],
                      [1,0,0,1,0],
                      [0,1,0,1,0],
                      [0,0,0,0,1],
                      [0,0,0,1,0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceEqual(graph.get_measure(MeasureTriangles, 'triangles').tolist(),
                                 [1, 2, 2, 1, 0])

    def test_graphWD(self):
        A = np.array([[0,0,0.1,0.8],
                      [0.5,0,0,0.2],
                      [0,0.1,0,0.4],
                      [0,0,0,0]])
        settings = GraphSettings(weighted = True, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureTriangles, 'triangles').tolist(),
                                       [0.1710, 0.1710, 0.1710, 0], places=4)

    def test_graphWU(self):
        A = np.array([[0,0.5,0.1,0.8],
                      [0.5,0,0.1,0.2],
                      [0.1,0.1,0,0.4],
                      [0.8,0.2,0.4,0]])
        settings = GraphSettings(weighted = True, directed = False, rule_standardize = 'range')
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureTriangles, 'triangles').tolist(),
                                       [1.1492, 1.0024, 0.8606, 1.1855], places=4)

if __name__ == '__main__':
    unittest.main()
