import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_distance import MeasureDistance
from braphy.graph import *
import numpy as np

class TestDistance(unittest.TestCase):
    def test_graphBU_disconnected(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        true_distance = [[0.0, 1.0, 1.0, np.inf], [1.0, 0.0, 2.0, np.inf],
                         [1.0, 2.0, 0.0, np.inf], [np.inf, np.inf, np.inf, 0.0]]
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

    def test_graphBU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 0, 1], [0, 0, 1], [1, 1, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        true_distance = [[0.0, 2.0, 1.0], [2.0, 0.0, 1.0], [1.0, 1.0, 0.0]]
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

    def test_graphBD_small(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBU], 'zero')
        true_distance = [[0.0, 1.0, 2.0], [2.0, 0.0, 1.0], [1.0, 2.0, 0.0]]
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

    def test_graphBD_large(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1],
                      [0, 0, 1, 0, 0], [1, 0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBU], 'zero')
        true_distance = [[0.0, 1.0, 2.0, 3.0, 3.0], [3.0, 0.0, 1.0, 2.0, 2.0],
                         [2.0, 3.0, 0.0, 1.0, 1.0], [3.0, 4.0, 1.0, 0.0, 2.0],
                         [1.0, 2.0, 3.0, 4.0, 0.0]]
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

    def test_graphWU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0.0, 0.1, 0.5, 0.4, 0.0],
                      [0.1, 0.0, 0.2, 0.5, 0.0],
                      [0.5, 0.2, 0.0, 0.4, 0.0],
                      [0.4, 0.5, 0.4, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0]])
        true_distance = [[0.0, 2.25, 1.0, 1.25, np.inf],
                         [2.25, 0.0, 2.25, 1.0, np.inf],
                         [1.0, 2.25, 0.0, 1.25, np.inf],
                         [1.25, 1.0, 1.25, 0.0, np.inf],
                         [np.inf, np.inf, np.inf, np.inf, 0]]
        graph = GraphWU(A, measure_list[GraphWU], 'zero', 'min')
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

    def test_graphWD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0.0, 0.1, 0.5, 0.4, 0.0],
                      [0.8, 0.0, 0.0, 0.0, 0.0],
                      [0.5, 0.2, 0.0, 0.4, 0.0],
                      [0.8, 0.1, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0]])
        true_distance = [[0.0, 5.6, 1.6, 2, np.inf],
                         [1, 0.0, 2.6, 3.0, np.inf],
                         [1.6, 4, 0.0, 2, np.inf],
                         [1, 6.6, 2.6, 0.0, np.inf],
                         [np.inf, np.inf, np.inf, np.inf, 0]]
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

    def test_BD_disconnected(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, 0, 1, 1, 1], [0, 1, 1, 0, 1], [1, 0, 1, 1, 1], [0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 1]])
        graph = GraphBD(A, measure_list[GraphBU], 'zero')
        true_distance = [[0.0, 2.0, 1.0, 1.0, 1.0], [2.0, 0.0, 1.0, 2.0, 1.0],
                         [1.0, 2.0, 0.0, 1.0, 1.0], [np.inf, np.inf, np.inf, 0.0, np.inf],
                         [2.0, 1.0, 1.0, 2.0, 0.0]]
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

if __name__ == '__main__':
    unittest.main()
