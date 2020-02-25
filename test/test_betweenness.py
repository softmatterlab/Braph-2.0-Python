import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_betweenness import MeasureBetweenness
from test.test_utility import TestUtility
from braphy.graph import *
import numpy as np

class TestBetweenness(TestUtility):
    def test_bd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        betweenness = [2, 0, 0]
        self.assertSequenceEqual(graph.get_measure(MeasureBetweenness, 'betweenness').tolist(),
                                 betweenness)

    def test_bd_2(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 0, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [1, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        betweenness = [4.0000, 2.5000, 4.0000, 2.5000, 12.0000, 2.5000, 2.5000, 0]
        self.assertSequenceEqual(graph.get_measure(MeasureBetweenness, 'betweenness').tolist(),
                                 betweenness)

    def test_bu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero')
        betweenness = [0.6667, 2.6667, 3.3333, 2.6667, 25.6667, 5.0000, 5.0000, 1.0000]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureBetweenness, 'betweenness'),
                                       betweenness, places = 4)

    def test_wd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        betweenness = [2., 0., 0.]
        self.assertSequenceEqual(graph.get_measure(MeasureBetweenness, 'betweenness').tolist(),
                                 betweenness)

    def test_wd2(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        betweenness = [0., 0., 12., 0., 12., 0., 5., 0.]
        self.assertSequenceEqual(graph.get_measure(MeasureBetweenness, 'betweenness').tolist(),
                                 betweenness)

    def test_wu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph = GraphWU(A, measure_list[GraphWU], 'zero')
        betweenness = [0, 0, 30, 0, 24, 0, 20, 12]
        self.assertSequenceEqual(graph.get_measure(MeasureBetweenness, 'betweenness').tolist(),
                                 betweenness)

if __name__ == '__main__':
    unittest.main()
