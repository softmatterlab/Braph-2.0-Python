import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_cluster import MeasureCluster
from braphy.graph import *
import numpy as np

class TestCluster(unittest.TestCase):
    def test_graphBD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,1,0,1,0,0,0,0],[0,0,1,0,1,0,0,0],[1,0,0,0,1,0,0,0],[0,0,1,0,1,0,0,0],
                      [0,0,0,0,0,1,1,0],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0]])
        graph_bd = GraphBD(A, measure_list[GraphBD], 'zero')
        MeasureCluster.compute_measure(graph_bd)
        for i in range(len(A[0])):
            self.assertAlmostEqual(graph_bd.measure_dict[MeasureCluster]['cluster'].tolist()[i], 
                                  [1.0000, 0.5000, 0.5000, 0.5000, 0, 0, 0, 0][i], places=4)

    def test_graphBU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,1,1,1,0,0,0,0],[0,0,1,0,1,0,0,0],[0,0,0,0,1,0,0,0],[0,0,1,0,1,0,0,0],
                     [0,0,0,0,0,1,1,0],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0]])
        graph_bu = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        MeasureCluster.compute_measure(graph_bu)
        for i in range(len(A[0])):
            self.assertAlmostEqual(graph_bu.measure_dict[MeasureCluster]['cluster'].tolist()[i], 
                                  [0.6667, 0.6667, 0.6667, 0.6667, 0.2000, 0, 0, 0][i], places=4)

    def test_graphWD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,0.1,0,0.1,0,0,0,0],[0,0,0.5,0,0.1,0,0,0],[0.2,0,0,0,0.2,0,0,0],
                      [0,0,0.5,0,0.1,0,0,0],[0,0,0,0,0,0.1,0.5,0],[0,0,0,0,0,0,0,0.2],
                      [0,0,0,0,0,0,0,0.8],[0,0,0,0,0,0,0,0]])
        graph_wd = GraphWD(A, measure_list[GraphWD], 'zero')
        MeasureCluster.compute_measure(graph_wd)
        for i in range(len(A[0])):
            self.assertAlmostEqual(graph_wd.measure_dict[MeasureCluster]['cluster'].tolist()[i], 
                                  [0.1077, 0.0539, 0.0539, 0.0539, 0, 0, 0, 0][i], places=4)

    def test_graphWU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,0.1,0.2,0.1,0,0,0,0],[0,0,0.5,0,0.1,0,0,0],[0,0,0,0,0.2,0,0,0],
                      [0,0,0.5,0,0.1,0,0,0],[0,0,0,0,0,0.1,0.5,0],[0,0,0,0,0,0,0,0.2],
                      [0,0,0,0,0,0,0,0.8],[0,0,0,0,0,0,0,0]])
        graph_wu = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        MeasureCluster.compute_measure(graph_wu)
        for i in range(len(A[0])):
            self.assertAlmostEqual(graph_wu.measure_dict[MeasureCluster]['cluster'].tolist()[i], 
                                   [0.1436, 0.1436, 0.1436, 0.1436, 0.0431, 0, 0, 0][i], places=4)

if __name__ == '__main__':
    unittest.main()
