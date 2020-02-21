import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_eccentricity import MeasureEccentricity
from braphy.graph import *
from test.test_utility import TestUtility
import numpy as np


class TestEccentricity(TestUtility):
    def test_graphBD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1],
                      [0, 0, 1, 0, 0], [1, 0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        in_eccentricity = [3, 4, 3, 4, 3]
        out_eccentricity = [3, 3, 3, 4, 4]
        eccentricity = [3, 4, 3, 4, 4]
        self.assertSequenceEqual(graph.get_measure(MeasureEccentricity, 'in_eccentricity').tolist(), in_eccentricity)
        self.assertSequenceEqual(graph.get_measure(MeasureEccentricity, 'out_eccentricity').tolist(), out_eccentricity)
        self.assertSequenceEqual(graph.get_measure(MeasureEccentricity, 'eccentricity').tolist(), eccentricity)

    def test_graphBU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1],
                      [0, 0, 1, 0, 0], [1, 0, 0, 0, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        eccentricity = [3, 2, 2, 3, 2]
        self.assertSequenceEqual(graph.get_measure(MeasureEccentricity, 'eccentricity').tolist(), eccentricity)

    def test_graphWD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0.0, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 0.0, 3.14, 6.7, 75],
                      [13, 0.0, 0.0, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0, 0.5],
                      [1, 0.0, 345, 8.7, 0.0]])
        graph = GraphWD(A, measure_list[GraphWD], 'abs')
        eccentricity = [0.4467, 0.3185, 0.3347, 0.4467, 0.3318]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureEccentricity, 'eccentricity'), eccentricity, places = 4)

    def test_graphWU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, 75],
                      [13, 0.0, 1.2, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0005, 0.5],
                      [1, 0.0, 345, 8.7, 2]])
        graph = GraphWU(A, measure_list[GraphWU], 'null', 'max')
        eccentricity = [0.1818, 0.1220, 0.1178, 0.1818, 0.1149]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureEccentricity, 'eccentricity'), eccentricity, places = 4)

if __name__ == '__main__':
    unittest.main()
