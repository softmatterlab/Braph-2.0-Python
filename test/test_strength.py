import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_strength import MeasureStrength
from braphy.graph import *
import numpy as np

class TestStrength(unittest.TestCase):
    def test_graphWD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0], [3.2, 2.7, 3.14, 6.7, -75],
                      [13, 0.0, 1.2, 5.7, -0.01], [5.5, 8.2, 0.3, 0.0005, -0.5],
                      [1, 0.0, 345, 8.7, -2]])
        graph_wd = GraphWD(A, measure_list[GraphWD], 'null')
        MeasureStrength.compute_measure(graph_wd)
        for i in range(len(A[0])):
            self.assertAlmostEqual(graph_wd.measure_dict[MeasureStrength]['strength'].tolist()[i], [28.55, -50.62, 369.83, 34.61, 279.19][i])
            self.assertAlmostEqual(graph_wd.measure_dict[MeasureStrength]['in_strength'].tolist()[i], [22.7, 11.34, 351.14, 21.11, -75.51][i])
            self.assertAlmostEqual(graph_wd.measure_dict[MeasureStrength]['out_strength'].tolist()[i], [5.85, -61.96, 18.69, 13.5, 354.7][i])
        self.assertAlmostEqual(graph_wd.measure_dict[MeasureStrength]['avg_strength'], 132.312)
        self.assertAlmostEqual(graph_wd.measure_dict[MeasureStrength]['avg_in_strength'], 66.156)
        self.assertAlmostEqual(graph_wd.measure_dict[MeasureStrength]['avg_out_strength'], 66.156)

    def test_graphWU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0], [3.2, 2.7, 3.14, 6.7, -75],
                      [13, 0.0, 1.2, 5.7, -0.01], [5.5, 8.2, 0.3, 0.0005, -0.5],
                      [1, 0.0, 345, 8.7, -2]])
        graph_wu = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        MeasureStrength.compute_measure(graph_wu)
        for i in range(len(A[0])):
            self.assertAlmostEqual(graph_wu.measure_dict[MeasureStrength]['strength'].tolist()[i], [22.7, 14.54, 366.84, 28.1, 354.7][i])
        self.assertAlmostEqual(graph_wu.measure_dict[MeasureStrength]['avg_strength'], 157.376)

if __name__ == '__main__':
    unittest.main()
