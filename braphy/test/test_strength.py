import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_strength import MeasureStrength
from braphy.test.test_utility import TestUtility
import numpy as np

class TestStrength(TestUtility):
    def test_graphWD(self):
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, -75],
                      [13, 0.0, 1.2, 5.7, -0.01],
                      [5.5, 8.2, 0.3, 0.0005, -0.5],
                      [1, 0.0, 345, 8.7, -2]])
        settings = GraphSettings(weighted = True, directed = True, rule_negative = 'null', rule_standardize = 'range')
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureStrength, 'in_strength').tolist(),
                                       [0.0658, 0.0329, 1.0178, 0.0612, 0], 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureStrength, 'out_strength').tolist(),
                                       [0.0170, 0.0378, 0.0542, 0.0406, 1.0281], 4)
        self.assertAlmostEqual(graph.get_measure(MeasureStrength, 'avg_in_strength'), 0.2355, 4)
        self.assertAlmostEqual(graph.get_measure(MeasureStrength, 'avg_out_strength'), 0.2355, 4)

    def test_graphWU(self):
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, -75],
                      [13, 0.0, 1.2, 5.7, -0.01],
                      [5.5, 8.2, 0.3, 0.0005, -0.5],
                      [1, 0.0, 345, 8.7, -2]])
        settings = GraphSettings(weighted = True, directed = False, rule_standardize = 'range')
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureStrength, 'strength').tolist(),
                                       [0.0658, 0.0421, 1.0633, 0.0814, 1.0281], 4)
        self.assertAlmostEqual(graph.get_measure(MeasureStrength, 'avg_strength'), 0.4562, 4)

if __name__ == '__main__':
    unittest.main()
