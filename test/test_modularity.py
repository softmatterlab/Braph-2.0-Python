import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_modularity import MeasureModularity
from braphy.graph import *
import numpy as np

class TestModularity(unittest.TestCase):
    def test_modularity_1(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        self.assertAlmostEqual(graph.get_measure(MeasureModularity, 'modularity'), 0, places = 4)

    def test_modularity_2(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        self.assertAlmostEqual(graph.get_measure(MeasureModularity, 'modularity'), 5.5511e-17,
                               places = 4)

    def test_modularity_3(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 999999, 999999, 0, 0, 0],
                      [999999, 0, 999999, 0, 0, 0],
                      [999999, 999999, 0, 1, 0, 0],
                      [0, 0, 1, 0, 999999, 999999],
                      [0, 0, 0, 999999, 0, 999999],
                      [0, 0, 0, 999999, 999999, 0]])
        graph = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        self.assertAlmostEqual(graph.get_measure(MeasureModularity, 'modularity'), 0.5, places = 4)

if __name__ == '__main__':
    unittest.main()
