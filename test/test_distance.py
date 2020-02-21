import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph import *
import numpy as np

class TestDistance(unittest.TestCase):
    def test_graphBU_disconnected(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        true_distance = [[0.0, 1.0, 1.0, np.inf], [1.0, 0.0, 2.0, np.inf],
                         [1.0, 2.0, 0.0, np.inf], [np.inf, np.inf, np.inf, 0.0]]
        self.assertSequenceEqual(graph.D.tolist(), true_distance)

    def test_graphBU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 0, 1], [0, 0, 1], [1, 1, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        true_distance = [[0.0, 2.0, 1.0], [2.0, 0.0, 1.0], [1.0, 1.0, 0.0]]
        self.assertSequenceEqual(graph.D.tolist(), true_distance)

    def test_graphBD_small(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBU], 'zero')
        true_distance = [[0.0, 1.0, 2.0], [2.0, 0.0, 1.0], [1.0, 2.0, 0.0]]
        self.assertSequenceEqual(graph.D.tolist(), true_distance)

    def test_graphBD_large(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1],
                      [0, 0, 1, 0, 0], [1, 0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBU], 'zero')
        true_distance = [[0.0, 1.0, 2.0, 3.0, 3.0], [3.0, 0.0, 1.0, 2.0, 2.0],
                         [2.0, 3.0, 0.0, 1.0, 1.0], [3.0, 4.0, 1.0, 0.0, 2.0],
                         [1.0, 2.0, 3.0, 4.0, 0.0]]
        self.assertSequenceEqual(graph.D.tolist(), true_distance)

    def test_graphWU(self):
    
        measure_list = MeasureParser.list_measures()
        A = np.array([[0.0, 0.1, 0.5, 0.4, 0.0],
                      [0.1, 0.0, 0.2, 0.5, 0.0],
                      [0.5, 0.2, 0.0, 0.4, 0.0],
                      [0.4, 0.5, 0.4, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0]])
        true_distance = [[0.0, 4.5, 2.0, 2.5, np.inf],
                         [4.5, 0.0, 4.5, 2.0, np.inf],
                         [2.0, 4.5, 0.0, 2.5, np.inf],
                         [2.5, 2.0, 2.5, 0.0, np.inf],
                         [np.inf, np.inf, np.inf, np.inf, 0]]
        graph = GraphWU(A, measure_list[GraphWU], 'zero', 'min')
        self.assertSequenceEqual(graph.D.tolist(), true_distance)

    def test_graphWD(self):
        
        measure_list = MeasureParser.list_measures()
        A = np.array([[0.0, 0.1, 0.5, 0.4, 0.0],
                      [0.8, 0.0, 0.0, 0.0, 0.0],
                      [0.5, 0.2, 0.0, 0.4, 0.0],
                      [0.8, 0.1, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0]])
        true_distance = [[0.0, 7.0, 2.0, 2.5, np.inf],
                         [1.25, 0.0, 3.25, 3.75, np.inf],
                         [2.0, 5.0, 0.0, 2.5, np.inf],
                         [1.25, 8.25, 3.25, 0.0, np.inf],
                         [np.inf, np.inf, np.inf, np.inf, 0]]
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        self.assertSequenceEqual(graph.D.tolist(), true_distance)

    def test_BD_disconnected(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, 0, 1, 1, 1], [0, 1, 1, 0, 1], [1, 0, 1, 1, 1], [0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 1]])
        graph = GraphBD(A, measure_list[GraphBU], 'zero')
        true_distance = [[0.0, 2.0, 1.0, 1.0, 1.0], [2.0, 0.0, 1.0, 2.0, 1.0],
                         [1.0, 2.0, 0.0, 1.0, 1.0], [np.inf, np.inf, np.inf, 0.0, np.inf],
                         [2.0, 1.0, 1.0, 2.0, 0.0]]
        self.assertSequenceEqual(graph.D.tolist(), true_distance)

if __name__ == '__main__':
    unittest.main()
