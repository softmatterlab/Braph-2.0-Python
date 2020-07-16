import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
import numpy as np

class TestGraphBU(unittest.TestCase):
    def test_binary(self):
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        self.assertTrue(graph.is_binary())

    def test_directed(self):
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        self.assertFalse(graph.is_directed())

    def test_remove_diagonal(self):
        A = np.array([[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        for (i, j), value in np.ndenumerate(graph.A):
            if(i == j):
                self.assertEqual(value, 0)

    def test_semipositivize(self):
        A = np.array([[1, -1, 1, -1], [1, -1, 1, 0], [-1, 1, 0, 0], [0, 0, 0, 0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        for (i, j), value in np.ndenumerate(graph.A):
            self.assertTrue(value >= 0)

    def test_symmetrize(self):
        A = np.array([[1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        for (i, j), value in np.ndenumerate(graph.A):
            if(i != j):
                self.assertTrue(value > 0)

    def test_binarize(self):
        A = np.array([[0, 0, 0, 0],
                      [4.3, 1.5, -2, 0],
                      [-600, 0.00, 3.14, 0],
                      [1, 1.0, 0.5, 0.0006]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        for (i, j), value in np.ndenumerate(graph.A):
            self.assertTrue(value == 1 or value == 0)

if __name__ == '__main__':
    unittest.main()
