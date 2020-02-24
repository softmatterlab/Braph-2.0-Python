import unittest
from braphy.graph_measures import MeasureParser
from braphy.graph import *
import numpy as np

class TestGraphBD(unittest.TestCase):
    def test_binary(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        self.assertTrue(graph.is_binary())

    def test_directed(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        self.assertTrue(graph.is_directed())

    def test_remove_diagonal(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        for (i, j), value in np.ndenumerate(graph.A):
            if(i == j):
                self.assertEqual(value, 0)

    def test_remove_negative_weights(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, -1, 1, -1], [1, -1, 1, 0], [-1, 1, 0, 0], [0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        for (i, j), value in np.ndenumerate(graph.A):
            self.assertTrue(value >= 0)

    def test_binarize(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, -6, 2, 0], [44, -15, 1, 0], [100, 0.6, 0, 0], [0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        for (i, j), value in np.ndenumerate(graph.A):
            self.assertTrue(value == 1 or value == 0)

if __name__ == '__main__':
    unittest.main()
