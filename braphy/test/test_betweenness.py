import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_betweenness import MeasureBetweenness
from braphy.test.test_utility import TestUtility
import numpy as np

class TestBetweenness(TestUtility):
    def test_bd(self):
        A = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
        settings = GraphSettings(weighted = False, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        betweenness = [2, 0, 0]
        self.assertSequenceEqual(graph.get_measure(MeasureBetweenness, 'betweenness').tolist(),
                                 betweenness)

    def test_bd_2(self):
        A = np.array([[0, 1, 0, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [1, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = False, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        betweenness = [4.0000, 2.5000, 4.0000, 2.5000, 12.0000, 2.5000, 2.5000, 0]
        self.assertSequenceEqual(graph.get_measure(MeasureBetweenness, 'betweenness').tolist(),
                                 betweenness)

    def test_bu(self):
        A = np.array([[0, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        betweenness = [0.6667, 2.6667, 3.3333, 2.6667, 25.6667, 5.0000, 5.0000, 1.0000]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureBetweenness, 'betweenness'),
                                       betweenness, places = 4)

    def test_wd(self):
        A = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
        settings = GraphSettings(weighted = True, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        betweenness = [2., 0., 0.]
        self.assertSequenceEqual(graph.get_measure(MeasureBetweenness, 'betweenness').tolist(),
                                 betweenness)

    def test_wd2(self):
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = True, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        betweenness = [0., 0., 12., 0., 12., 0., 5., 0.]
        self.assertSequenceEqual(graph.get_measure(MeasureBetweenness, 'betweenness').tolist(),
                                 betweenness)

    def test_wu(self):
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = True, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        betweenness = [0, 0, 30, 0, 24, 0, 20, 12]
        self.assertSequenceEqual(graph.get_measure(MeasureBetweenness, 'betweenness').tolist(),
                                 betweenness)
        
if __name__ == '__main__':
    unittest.main()
