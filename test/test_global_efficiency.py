import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_global_efficiency import MeasureGlobalEfficiency
from braphy.graph import *
from test.test_utility import TestUtility
import numpy as np

class TestGlobalEfficiency(unittest.TestCase):
    def test_bd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, 1, 0, 1],
                      [1, 0, 1, 1],
                      [1, 0, 1, 1],
                      [0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        MeasureGlobalEfficiency.compute_measure(graph)
        global_efficiency = [0.75, 0.75, 0.6667, 0.5]
        in_global_efficiency = [0.6667, 0.5, 0.5, 1.0]
        out_global_efficiency = [0.8333, 1.0, 0.8333, 0]
        test_utility = TestUtility()
        test_utility.assertSequenceAlmostEqual(graph.measure_dict[MeasureGlobalEfficiency]
                                              ['global_efficiency'].tolist(), global_efficiency, 4)
        test_utility.assertSequenceAlmostEqual(graph.measure_dict[MeasureGlobalEfficiency]
                                              ['in_global_efficiency'].tolist(), in_global_efficiency, 4)
        test_utility.assertSequenceAlmostEqual(graph.measure_dict[MeasureGlobalEfficiency]
                                              ['out_global_efficiency'].tolist(), out_global_efficiency, 4)

    def test_bu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, 1, 0, 1],
                      [1, 0, 1, 1],
                      [1, 0, 1, 1],
                      [0, 0, 0, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        MeasureGlobalEfficiency.compute_measure(graph)
        global_efficiency = [1, 1, 1, 1]
        test_utility = TestUtility()
        test_utility.assertSequenceAlmostEqual(graph.measure_dict[MeasureGlobalEfficiency]
                                              ['global_efficiency'].tolist(), global_efficiency, 4)

    def test_wd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0.7577,    0.7060,    0.8235,    0.4387,    0.4898],
                      [0.7431,    0.0318,    0.6948,    0.3816,    0.4456],
                      [0.3922,    0.2769,    0.3171,    0.7655,    0.6463],
                      [0.6555,    0.0462,    0.9502,    0.7952,    0.7094],
                      [0.1712,    0.0971,    0.0344,    0.1869,    0.7547]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        MeasureGlobalEfficiency.compute_measure(graph)
        global_efficiency = [0.5525,    0.4657,    0.5882,    0.5535,    0.3679]
        in_global_efficiency = [0.4905,    0.3652,    0.6562,    0.4432,    0.5728]
        out_global_efficiency = [0.6145,    0.5663,    0.5202,    0.6637,    0.1630]
        test_utility = TestUtility()
        test_utility.assertSequenceAlmostEqual(graph.measure_dict[MeasureGlobalEfficiency]
                                              ['global_efficiency'].tolist(), global_efficiency, 4)
        test_utility.assertSequenceAlmostEqual(graph.measure_dict[MeasureGlobalEfficiency]
                                              ['in_global_efficiency'].tolist(), in_global_efficiency, 3)
        test_utility.assertSequenceAlmostEqual(graph.measure_dict[MeasureGlobalEfficiency]
                                              ['out_global_efficiency'].tolist(), out_global_efficiency, 3)

    def test_wu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0.7577,    0.7060,    0.8235,    0.4387,    0.4898],
                      [0.7431,    0.0318,    0.6948,    0.3816,    0.4456],
                      [0.3922,    0.2769,    0.3171,    0.7655,    0.6463],
                      [0.6555,    0.0462,    0.9502,    0.7952,    0.7094],
                      [0.1712,    0.0971,    0.0344,    0.1869,    0.7547]])
        graph = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        MeasureGlobalEfficiency.compute_measure(graph)
        global_efficiency = [0.6780,    0.5712,    0.7787,    0.6791,    0.5728]
        test_utility = TestUtility()
        test_utility.assertSequenceAlmostEqual(graph.measure_dict[MeasureGlobalEfficiency]
                                              ['global_efficiency'].tolist(), global_efficiency, 4)

if __name__ == '__main__':
    unittest.main()
