import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_eccentricity import MeasureEccentricity
from braphy.test.test_utility import TestUtility
import numpy as np


class TestEccentricity(TestUtility):
    def test_graphBD(self):
        A = np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1],
                      [0, 0, 1, 0, 0], [1, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = False, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        in_eccentricity = [3, 4, 3, 4, 3]
        out_eccentricity = [3, 3, 3, 4, 4]
        eccentricity = [3, 4, 3, 4, 4]
        self.assertSequenceEqual(graph.get_measure(MeasureEccentricity,
                                                   'in_eccentricity').tolist(), in_eccentricity)
        self.assertSequenceEqual(graph.get_measure(MeasureEccentricity,
                                                   'out_eccentricity').tolist(), out_eccentricity)
        self.assertSequenceEqual(graph.get_measure(MeasureEccentricity,
                                                   'eccentricity').tolist(), eccentricity)

    def test_graphBU(self):
        A = np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1],
                      [0, 0, 1, 0, 0], [1, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        eccentricity = [3, 2, 2, 3, 2]
        self.assertSequenceEqual(graph.get_measure(MeasureEccentricity,
                                                   'eccentricity').tolist(), eccentricity)

    def test_graphWD(self):
        A = np.array([[0.0, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 0.0, 3.14, 6.7, 75],
                      [13, 0.0, 0.0, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0, 0.5],
                      [1, 0.0, 345, 8.7, 0.0]])
        settings = GraphSettings(weighted = True, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        eccentricity = [154.1278, 109.8726, 115.4726, 154.1278, 114.4726]
        in_eccentricity = [62.7273, 109.8726, 115.4726, 154.1278, 114.4726]
        out_eccentricity = [154.1278, 44.2552, 107.1995, 62.7273, 81.7283]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureEccentricity,
                                                         'eccentricity'),
                                                         eccentricity, places = 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureEccentricity,
                                                         'in_eccentricity'),
                                                         in_eccentricity, places = 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureEccentricity,
                                                         'out_eccentricity'),
                                                         out_eccentricity, places = 4)

    def test_graphWU(self):
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, 75],
                      [13, 0.0, 1.2, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0005, 0.5],
                      [1, 0.0, 345, 8.7, 2]])
        settings = GraphSettings(weighted = True, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        eccentricity = [62.7273, 42.0732, 40.6552, 62.7273, 39.6552]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureEccentricity,
                                                         'eccentricity'), eccentricity, places = 4)

if __name__ == '__main__':
    unittest.main()
