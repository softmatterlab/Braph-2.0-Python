import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_closeness import MeasureCloseness
from braphy.test.test_utility import TestUtility
import numpy as np

class TestCloseness(TestUtility):
    def test_bd(self):
        A = np.array([[1, 0, 1, 1, 1],
                      [0, 1, 1, 0, 1],
                      [1, 0, 1, 1, 1],
                      [0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 1]])
        settings = GraphSettings(weighted = False, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        closeness = [1/1.458333, 1/1.5833, 1/1.1250, np.nan, 1/1.2500]
        closeness_in = [1/1.6667, 1/1.6667, 1/1.0, 1/1.5, 1/1.0]
        closeness_out = [1/1.25, 1/1.5, 1/1.25, np.nan, 1/1.5]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness').tolist(),
                                       closeness, 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness_in').tolist(),
                                       closeness_in, 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness_out').tolist(),
                                       closeness_out, 4)

    def test_bu(self):
        A = np.array([[1, 0, 1, 1, 1],
                      [0, 1, 1, 0, 1],
                      [1, 0, 1, 1, 1],
                      [0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 1]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        closeness = [1/1.25, 1/1.5, 1/1.0, 1/1.5, 1/1.25]
        self.assertSequenceEqual(graph.get_measure(MeasureCloseness, 'closeness').tolist(),
                                 closeness)

    def test_wd(self):
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, 75],
                      [13, 0.0, 1.2, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0005, 0.5],
                      [1, 0.0, 345, 8.7, 2]])
        settings = GraphSettings(weighted = True, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        closeness = [0.0124, 0.0189, 0.0171, 0.0161, 0.0189]
        closeness_in = [0.0269, 0.0119, 0.0236, 0.0134, 0.0147]
        closeness_out = [0.0081, 0.0462, 0.0135, 0.0201, 0.0267
]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness').tolist(),
                                       closeness, 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness_in').tolist(),
                                       closeness_in, 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness_out').tolist(),
                                       closeness_out, 4)

    def test_wu(self):
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, 75],
                      [13, 0.0, 1.2, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0005, 0.5],
                      [1, 0.0, 345, 8.7, 2]])
        settings = GraphSettings(weighted = True, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        closeness = [0.0269, 0.0474, 0.0542, 0.0216, 0.0549]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness').tolist(),
                                       closeness, places = 4)

    def test_wu_2(self):
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
        closeness = [0.1207, 0.1606, 0.2059, 0.1606, 0.2059, 0.1074, 0.1882, 0.1699]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureCloseness, 'closeness').tolist(),
                                       closeness, places = 4)


if __name__ == '__main__':
    unittest.main()
