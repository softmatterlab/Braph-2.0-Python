import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_triangles import MeasureTriangles
from braphy.graph import *
from test.test_utility import TestUtility
import numpy as np

class TestTriangles(TestUtility):
    def test_graphBD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,0,1,0],
                      [1,0,0,1],
                      [0,1,0,1],
                      [0,0,0,0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        self.assertSequenceEqual(graph.get_measure(MeasureTriangles, 'triangles').tolist(),
                                 [1, 1, 1, 0])

    def test_graphBU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,0,1,0,0],
                      [1,0,0,1,0],
                      [0,1,0,1,0],
                      [0,0,0,0,1],
                      [0,0,0,1,0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        self.assertSequenceEqual(graph.get_measure(MeasureTriangles, 'triangles').tolist(),
                                 [1, 2, 2, 1, 0])

    def test_graphWD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,0,0.1,0.8],
                      [0.5,0,0,0.2],
                      [0,0.1,0,0.4],
                      [0,0,0,0]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureTriangles, 'triangles').tolist(),
                                       [0.1069, 0.1069, 0.1069, 0], places=4)

    def test_graphWU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0,0.5,0.1,0.8],
                      [0.5,0,0.1,0.2],
                      [0.1,0.1,0,0.4],
                      [0.8,0.2,0.4,0]])
        graph = GraphWU(A, measure_list[GraphWU])
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureTriangles, 'triangles').tolist(),
                                       [1.1492, 1.0024, 0.8606, 1.1855], places=4)

if __name__ == '__main__':
    unittest.main()
