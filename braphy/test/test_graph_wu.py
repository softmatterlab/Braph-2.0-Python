import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
import numpy as np

class TestGraphWU(unittest.TestCase):
    def test_binary(self):
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        settings = GraphSettings.get_wu()
        graph = GraphFactory.get_graph(A, settings)
        self.assertFalse(graph.is_binary())

    def test_directed(self):
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        settings = GraphSettings.get_wu()
        graph = GraphFactory.get_graph(A, settings)
        self.assertFalse(graph.is_directed())

    def test_remove_diagonal(self):
        A = np.array([[1, 1, 1, 1], [1, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]])
        settings = GraphSettings.get_wu()
        graph = GraphFactory.get_graph(A, settings)
        for (i, j), value in np.ndenumerate(graph.A):
            if(i == j):
                self.assertEqual(value, 0)

    def test_semipositivize(self):
        A = np.array([[1, -1, 1, -1], [1, -1, 1, 0], [-1, 1, 0, 0], [0, 0, 0, 0]])
        settings = GraphSettings.get_wu()
        graph = GraphFactory.get_graph(A, settings)
        for (i, j), value in np.ndenumerate(graph.A):
            self.assertTrue(value >= 0)

    def test_symmetrize(self):
        A = np.array([[1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1]])
        settings = GraphSettings.get_wu()
        graph = GraphFactory.get_graph(A, settings)
        for (i, j), value in np.ndenumerate(graph.A):
            if(i != j):
                self.assertTrue(value > 0)

    def test_standardize(self):
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, 75],
                      [13, 0.0, 1.2, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0005, 0.5],
                      [1, 0.0, 345, 8.7, 2]])
        settings = GraphSettings.get_wu()
        graph = GraphFactory.get_graph(A, settings)
        self.assertTrue(np.min(graph.A) >= 0)
        self.assertTrue(np.max(graph.A) <= 1)

    def test_standardize_2(self):
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, 75],
                      [13, 0.0, 1.2, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0005, 0.5],
                      [1, 0.0, 345, 8.7, 2]])
        settings = GraphSettings.get_wu()
        graph = GraphFactory.get_graph(A, settings)
        self.assertTrue(np.min(graph.A) >= 0)
        self.assertTrue(np.max(graph.A) <= 1)

if __name__ == '__main__':
    unittest.main()
