import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_transitivity import MeasureTransitivity
import numpy as np

class TestTransitivity(unittest.TestCase):
    def test_bd(self):
        A = np.array([[0, 1, 1, 0],
                      [1, 0, 1, 0],
                      [1, 1, 0, 1],
                      [0, 0, 1, 0]])
        settings = GraphSettings(weighted = False, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        self.assertAlmostEqual(graph.get_measure(MeasureTransitivity, 'transitivity'), 0.15)

    def test_bu(self):
        A = np.array([[0, 1, 1, 0],
                      [1, 0, 1, 0],
                      [1, 1, 0, 1],
                      [0, 0, 1, 0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        self.assertAlmostEqual(graph.get_measure(MeasureTransitivity, 'transitivity'), 0.6)

    def test_wd(self):
        A = np.array([[0,0,0.1,0.8],
                      [0.5,0,0,0.2],
                      [0,0.1,0,0.4],
                      [0,0,0,0]])
        settings = GraphSettings(weighted = True, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        self.assertAlmostEqual(graph.get_measure(MeasureTransitivity, 'transitivity'), 0.0214, 4)

    def test_wu(self):
        A = np.array([[0,0,0.1,0.8],
                      [0.5,0,0,0.2],
                      [0,0.1,0,0.4],
                      [0,0,0,0]])
        settings = GraphSettings(weighted = True, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        self.assertAlmostEqual(graph.get_measure(MeasureTransitivity, 'transitivity'), 0.2798, 4)

if __name__ == '__main__':
    unittest.main()
