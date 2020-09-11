import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_cluster import MeasureCluster
from braphy.test.test_utility import TestUtility
import numpy as np

class TestCluster(TestUtility):
    def test_graphBD(self):
        A = np.array([[0,1,0,1,0,0,0,0],
                      [0,0,1,0,1,0,0,0],
                      [1,0,0,0,1,0,0,0],
                      [0,0,1,0,1,0,0,0],
                      [0,0,0,0,0,1,1,0],
                      [0,0,0,0,0,0,0,1],
                      [0,0,0,0,0,0,0,1],
                      [0,0,0,0,0,0,0,0]])
        settings = GraphSettings(weighted = False, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCluster, 'cluster').tolist(),
                                       [1.0000, 0.5000, 0.5000, 0.5000, 0, 0, 0, 0], places=4)

    def test_graphBU(self):
        A = np.array([[0,1,1,1,0,0,0,0],
                      [0,0,1,0,1,0,0,0],
                      [0,0,0,0,1,0,0,0],
                      [0,0,1,0,1,0,0,0],
                      [0,0,0,0,0,1,1,0],
                      [0,0,0,0,0,0,0,1],
                      [0,0,0,0,0,0,0,1],
                      [0,0,0,0,0,0,0,0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCluster, 'cluster').tolist(),
                                       [0.6667, 0.6667, 0.6667, 0.6667, 0.2000, 0, 0, 0], places=4)

    def test_graphWD(self):
        A = np.array([[0,0.1,0,0.1,0,0,0,0],
                      [0,0,0.5,0,0.1,0,0,0],
                      [0.2,0,0,0,0.2,0,0,0],
                      [0,0,0.5,0,0.1,0,0,0],
                      [0,0,0,0,0,0.1,0.5,0],
                      [0,0,0,0,0,0,0,0.2],
                      [0,0,0,0,0,0,0,0.8],
                      [0,0,0,0,0,0,0,0]])
        settings = GraphSettings(weighted = True, directed = True, rule_standardize = 'range')
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCluster, 'cluster').tolist(),
                                       [0.1347, 0.0673, 0.0673, 0.0673, 0, 0, 0, 0], places=4)

    def test_graphWU(self):
        A = np.array([[0,0.1,0.2,0.1,0,0,0,0],
                      [0,0,0.5,0,0.1,0,0,0],
                      [0,0,0,0,0.2,0,0,0],
                      [0,0,0.5,0,0.1,0,0,0],
                      [0,0,0,0,0,0.1,0.5,0],
                      [0,0,0,0,0,0,0,0.2],
                      [0,0,0,0,0,0,0,0.8],
                      [0,0,0,0,0,0,0,0]])
        settings = GraphSettings(weighted = True, directed = False, rule_standardize = 'range')
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCluster, 'cluster').tolist(),
                                       [0.1795, 0.1795, 0.1795, 0.1795, 0.0539, 0, 0, 0], places=4)

if __name__ == '__main__':
    unittest.main()
