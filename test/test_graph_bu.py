import unittest
from braphy.graph_measures import MeasureParser
from braphy.graph import *
import numpy as np

class TestGraphBU(unittest.TestCase):
    def test_binary(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        self.assertTrue(graph.is_binary())

    def test_directed(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        self.assertFalse(graph.is_directed())

    def test_remove_diagonal(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        for (i, j), value in np.ndenumerate(graph.A):
            if(i == j):
                self.assertEqual(value, 0)

    def test_remove_negative_weights(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, -1, 1, -1], [1, -1, 1, 0], [-1, 1, 0, 0], [0, 0, 0, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        for (i, j), value in np.ndenumerate(graph.A):
            self.assertTrue(value >= 0)

    def test_symmetrize(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        for (i, j), value in np.ndenumerate(graph.A):
            if(i != j):
                self.assertTrue(value > 0)

    def test_binarize(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 0, 0, 0],
                      [4.3, 1.5, -2, 0],
                      [-600, 0.00, 3.14, 0],
                      [1, 1.0, 0.5, 0.0006]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero')
        for (i, j), value in np.ndenumerate(graph.A):
            self.assertTrue(value == 1 or value == 0)

if __name__ == '__main__':
    unittest.main()
