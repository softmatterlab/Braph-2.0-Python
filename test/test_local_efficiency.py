import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_local_efficiency import MeasureLocalEfficiency
from braphy.graph import *
from test.test_utility import TestUtility
import numpy as np

class TestLocalEfficiency(TestUtility):
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
        local_efficiency = [0.3333, 0.3333, 0.3750, 0.3333, 0.1000, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureLocalEfficiency,
                                       'local_efficiency').tolist(), local_efficiency, 4)

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
        local_efficiency = [0.8333, 0.8333, 0.8333, 0.8333, 0.2500, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureLocalEfficiency,
                                       'local_efficiency').tolist(), local_efficiency, 4)

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
        local_efficiency = [0, 0, 0.0117, 0, 0.0156, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureLocalEfficiency,
                                       'local_efficiency').tolist(), local_efficiency, 4)

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
        local_efficiency = [0.1595, 0.1353, 0.0992, 0.1353, 0.1105, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureLocalEfficiency,
                                       'local_efficiency').tolist(), local_efficiency, 4)

if __name__ == '__main__':
    unittest.main()
