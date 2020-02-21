import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_local_efficiency import MeasureLocalEfficiency
from braphy.graph import *
from test.test_utility import TestUtility
import numpy as np

class TestLocalEfficiency(unittest.TestCase):
    def test_bd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 0, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [1, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        MeasureLocalEfficiency.compute_measure(graph)
        local_efficiency = [0.3333, 0.3333, 0.3750, 0.3333, 0.1000, 0, 0, 0]
        test_utility = TestUtility()
        test_utility.assertSequenceAlmostEqual(graph.measure_dict[MeasureLocalEfficiency]
                                              ['local_efficiency'].tolist(), local_efficiency, 4)

    def test_bu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 0, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [1, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        MeasureLocalEfficiency.compute_measure(graph)
        local_efficiency = [0.8333, 0.8333, 0.8333, 0.8333, 0.2500, 0, 0, 0]
        test_utility = TestUtility()
        test_utility.assertSequenceAlmostEqual(graph.measure_dict[MeasureLocalEfficiency]
                                              ['local_efficiency'].tolist(), local_efficiency, 4)

    def test_wd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0.2, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        MeasureLocalEfficiency.compute_measure(graph)
        local_efficiency = [0, 0, 0.0075, 0, 0.0100, 0, 0, 0]
        test_utility = TestUtility()
        test_utility.assertSequenceAlmostEqual(graph.measure_dict[MeasureLocalEfficiency]
                                              ['local_efficiency'].tolist(), local_efficiency, 4)

    def test_wu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0.2, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        MeasureLocalEfficiency.compute_measure(graph)
        local_efficiency = [0.1021, 0.0866, 0.0635, 0.0866, 0.0707, 0, 0, 0]
        test_utility = TestUtility()
        test_utility.assertSequenceAlmostEqual(graph.measure_dict[MeasureLocalEfficiency]
                                              ['local_efficiency'].tolist(), local_efficiency, 4)

if __name__ == '__main__':
    unittest.main()
