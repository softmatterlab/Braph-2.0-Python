import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.graph_measures.measure_distance import MeasureDistance
import numpy as np

class TestDistance(unittest.TestCase):
    def test_graphBU_disconnected(self):
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        settings = GraphSettings.get_bu()
        graph = GraphFactory.get_graph(A, settings)
        true_distance = [[0.0, 1.0, 1.0, np.inf], [1.0, 0.0, 2.0, np.inf],
                         [1.0, 2.0, 0.0, np.inf], [np.inf, np.inf, np.inf, 0.0]]
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

    def test_graphBU(self):
        A = np.array([[0, 0, 1], [0, 0, 1], [1, 1, 0]])
        settings = GraphSettings.get_bu()
        graph = GraphFactory.get_graph(A, settings)
        true_distance = [[0.0, 2.0, 1.0], [2.0, 0.0, 1.0], [1.0, 1.0, 0.0]]
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

    def test_graphBD_small(self):
        A = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)
        true_distance = [[0.0, 1.0, 2.0], [2.0, 0.0, 1.0], [1.0, 2.0, 0.0]]
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

    def test_graphBD_large(self):
        A = np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1],
                      [0, 0, 1, 0, 0], [1, 0, 0, 0, 0]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)
        true_distance = [[0.0, 1.0, 2.0, 3.0, 3.0], [3.0, 0.0, 1.0, 2.0, 2.0],
                         [2.0, 3.0, 0.0, 1.0, 1.0], [3.0, 4.0, 1.0, 0.0, 2.0],
                         [1.0, 2.0, 3.0, 4.0, 0.0]]
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

    def test_graphWU(self):
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
        settings = GraphSettings.get_wu()
        graph = GraphFactory.get_graph(A, settings)
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

    def test_graphWD(self):
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
        settings = GraphSettings.get_wd()
        graph = GraphFactory.get_graph(A, settings)
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

    def test_BD_disconnected(self):
        A = np.array([[1, 0, 1, 1, 1], [0, 1, 1, 0, 1], [1, 0, 1, 1, 1], [0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 1]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)
        true_distance = [[0.0, 2.0, 1.0, 1.0, 1.0], [2.0, 0.0, 1.0, 2.0, 1.0],
                         [1.0, 2.0, 0.0, 1.0, 1.0], [np.inf, np.inf, np.inf, 0.0, np.inf],
                         [2.0, 1.0, 1.0, 2.0, 0.0]]
        D = graph.get_measure(MeasureDistance, 'distance')
        self.assertSequenceEqual(D.tolist(), true_distance)

if __name__ == '__main__':
    unittest.main()
