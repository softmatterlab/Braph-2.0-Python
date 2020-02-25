import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_strength import MeasureStrength
from braphy.graph import *
from test.test_utility import TestUtility
import numpy as np

class TestStrength(TestUtility):
    def test_graphWD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, -75],
                      [13, 0.0, 1.2, 5.7, -0.01],
                      [5.5, 8.2, 0.3, 0.0005, -0.5],
                      [1, 0.0, 345, 8.7, -2]])
        graph = GraphWD(A, measure_list[GraphWD], 'null')
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureStrength, 'strength').tolist(),
                                       [1.4965, 1.3080, 2.3091, 1.5110, 2.0933], 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureStrength, 'in_strength').tolist(),
                                       [0.7683, 0.7413, 1.5503, 0.7645, 0.5345], 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureStrength, 'out_strength').tolist(),
                                       [0.7282, 0.5668, 0.7588, 0.7464, 1.5588], 4)
        self.assertAlmostEqual(graph.get_measure(MeasureStrength, 'avg_strength'), 1.7436)
        self.assertAlmostEqual(graph.get_measure(MeasureStrength, 'avg_in_strength'), 0.8718)
        self.assertAlmostEqual(graph.get_measure(MeasureStrength, 'avg_out_strength'), 0.8718)

    def test_graphWU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, -75],
                      [13, 0.0, 1.2, 5.7, -0.01],
                      [5.5, 8.2, 0.3, 0.0005, -0.5],
                      [1, 0.0, 345, 8.7, -2]])
        graph = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureStrength, 'strength').tolist(),
                                       [0.0658, 0.0421, 1.0633, 0.0814, 1.0281], 4)
        self.assertAlmostEqual(graph.get_measure(MeasureStrength, 'avg_strength'), 0.4562, 4)

if __name__ == '__main__':
    unittest.main()
