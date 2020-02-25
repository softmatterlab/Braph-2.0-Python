import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_cluster import MeasureCluster
from braphy.graph import *
from test.test_utility import TestUtility
import numpy as np

class TestCluster(TestUtility):
    def test_graphBD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,1,0,1,0,0,0,0],
                      [0,0,1,0,1,0,0,0],
                      [1,0,0,0,1,0,0,0],
                      [0,0,1,0,1,0,0,0],
                      [0,0,0,0,0,1,1,0],
                      [0,0,0,0,0,0,0,1],
                      [0,0,0,0,0,0,0,1],
                      [0,0,0,0,0,0,0,0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCluster, 'cluster').tolist(),
                                       [1.0000, 0.5000, 0.5000, 0.5000, 0, 0, 0, 0], places=4)

    def test_graphBU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,1,1,1,0,0,0,0],
                      [0,0,1,0,1,0,0,0],
                      [0,0,0,0,1,0,0,0],
                      [0,0,1,0,1,0,0,0],
                      [0,0,0,0,0,1,1,0],
                      [0,0,0,0,0,0,0,1],
                      [0,0,0,0,0,0,0,1],
                      [0,0,0,0,0,0,0,0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCluster, 'cluster').tolist(),
                                       [0.6667, 0.6667, 0.6667, 0.6667, 0.2000, 0, 0, 0], places=4)

    def test_graphWD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,0.1,0,0.1,0,0,0,0],
                      [0,0,0.5,0,0.1,0,0,0],
                      [0.2,0,0,0,0.2,0,0,0],
                      [0,0,0.5,0,0.1,0,0,0],
                      [0,0,0,0,0,0.1,0.5,0],
                      [0,0,0,0,0,0,0,0.2],
                      [0,0,0,0,0,0,0,0.8],
                      [0,0,0,0,0,0,0,0]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCluster, 'cluster').tolist(),
                                       [0.1347, 0.0673, 0.0673, 0.0673, 0, 0, 0, 0], places=4)

    def test_graphWU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,0.1,0.2,0.1,0,0,0,0],
                      [0,0,0.5,0,0.1,0,0,0],
                      [0,0,0,0,0.2,0,0,0],
                      [0,0,0.5,0,0.1,0,0,0],
                      [0,0,0,0,0,0.1,0.5,0],
                      [0,0,0,0,0,0,0,0.2],
                      [0,0,0,0,0,0,0,0.8],
                      [0,0,0,0,0,0,0,0]])
        graph = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCluster, 'cluster').tolist(),
                                       [0.1795, 0.1795, 0.1795, 0.1795, 0.0539, 0, 0, 0], places=4)

if __name__ == '__main__':
    unittest.main()
