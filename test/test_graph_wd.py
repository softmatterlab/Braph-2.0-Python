import unittest
from braphy.graph_measures import MeasureParser
from braphy.graph import *
import numpy as np

class TestGraphWD(unittest.TestCase):
    def test_binary(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        self.assertFalse(graph.is_binary())

    def test_directed(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        self.assertTrue(graph.is_directed())

    def test_remove_diagonal(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        for (i, j), value in np.ndenumerate(graph.A):
            if(i == j):
                self.assertEqual(value, 0)

    def test_remove_negative_weights(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, -1, 1, -1], [1, -1, 1, 0], [-1, 1, 0, 0], [0, 0, 0, 0]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        for (i, j), value in np.ndenumerate(graph.A):
            self.assertTrue(value >= 0)

    def test_standardize(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 2, 4], [0, 1, 1, 0], [3, 3, 3, 3], [0, 0, 0, 0]])
        graph = GraphWD(A, measure_list[GraphWD], rule_standardize = 'range')
        self.assertTrue(np.min(graph.A) >= 0)
        self.assertTrue(np.max(graph.A) <= 1)

    def test_standardize_2(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 2, 4], [0, 1, 1, 0], [3, 3, 3, 3], [0, 0, 0, 0]])
        graph = GraphWD(A, measure_list[GraphWD], rule_standardize = '1')
        self.assertTrue(np.min(graph.A) >= 0)
        self.assertTrue(np.max(graph.A) <= 1)

if __name__ == '__main__':
    unittest.main()
