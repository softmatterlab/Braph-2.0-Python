import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.graph_measures.measure_transitivity import MeasureTransitivity
import numpy as np

class TestTransitivity(unittest.TestCase):
    def test_bd(self):
        A = np.array([[0, 1, 1, 0],
                      [1, 0, 1, 0],
                      [1, 1, 0, 1],
                      [0, 0, 1, 0]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)
        self.assertAlmostEqual(graph.get_measure(MeasureTransitivity, 'transitivity'), 0.45)

    def test_bu(self):
        A = np.array([[0, 1, 1, 0],
                      [1, 0, 1, 0],
                      [1, 1, 0, 1],
                      [0, 0, 1, 0]])
        settings = GraphSettings.get_bu()
        graph = GraphFactory.get_graph(A, settings)
        self.assertAlmostEqual(graph.get_measure(MeasureTransitivity, 'transitivity'), 0.6)

    def test_wd(self):
        A = np.array([[0, 1, 1, 0],
                      [1, 0, 1, 0],
                      [1, 1, 0, 1],
                      [0, 0, 1, 0]])
        settings = GraphSettings.get_wd()
        graph = GraphFactory.get_graph(A, settings)
        self.assertAlmostEqual(graph.get_measure(MeasureTransitivity, 'transitivity'), 0.225)

    def test_wu(self):
        A = np.array([[0, 1, 1, 0],
                      [1, 0, 1, 0],
                      [1, 1, 0, 1],
                      [0, 0, 1, 0]])
        settings = GraphSettings.get_wu()
        graph = GraphFactory.get_graph(A, settings)
        self.assertAlmostEqual(graph.get_measure(MeasureTransitivity, 'transitivity'), 0.9)

if __name__ == '__main__':
    unittest.main()