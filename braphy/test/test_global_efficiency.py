import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.graph_measures.measure_global_efficiency import MeasureGlobalEfficiency
from braphy.test.test_utility import TestUtility
import numpy as np

class TestGlobalEfficiency(TestUtility):
    def test_bd(self):
        A = np.array([[1, 1, 0, 1],
                      [1, 0, 1, 1],
                      [1, 0, 1, 1],
                      [0, 0, 0, 0]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)
        global_efficiency = [0.75, 0.75, 0.6667, 0.5]
        in_global_efficiency = [0.6667, 0.5, 0.5, 1.0]
        out_global_efficiency = [0.8333, 1.0, 0.8333, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureGlobalEfficiency,
                                       'global_efficiency').tolist(), global_efficiency, 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureGlobalEfficiency,
                                       'in_global_efficiency').tolist(), in_global_efficiency, 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureGlobalEfficiency,
                                       'out_global_efficiency').tolist(), out_global_efficiency, 4)

    def test_bu(self):
        A = np.array([[1, 1, 0, 1],
                      [1, 0, 1, 1],
                      [1, 0, 1, 1],
                      [0, 0, 0, 0]])
        settings = GraphSettings.get_bu()
        graph = GraphFactory.get_graph(A, settings)
        global_efficiency = [1, 1, 1, 1]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureGlobalEfficiency,
                                       'global_efficiency').tolist(), global_efficiency, 4)

    def test_wd(self):
        A = np.array([[0.7577,    0.7060,    0.8235,    0.4387,    0.4898],
                      [0.7431,    0.0318,    0.6948,    0.3816,    0.4456],
                      [0.3922,    0.2769,    0.3171,    0.7655,    0.6463],
                      [0.6555,    0.0462,    0.9502,    0.7952,    0.7094],
                      [0.1712,    0.0971,    0.0344,    0.1869,    0.7547]])
        settings = GraphSettings.get_wd()
        graph = GraphFactory.get_graph(A, settings)
        global_efficiency = [0.5815, 0.4901, 0.6190, 0.5825, 0.3872]
        in_global_efficiency = [0.5162, 0.3843, 0.6906, 0.4664, 0.6028]
        out_global_efficiency = [0.6467, 0.5960, 0.5475, 0.6985, 0.1716]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureGlobalEfficiency,
                                       'global_efficiency').tolist(), global_efficiency, 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureGlobalEfficiency,
                                       'in_global_efficiency').tolist(), in_global_efficiency, 3)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureGlobalEfficiency,
                                       'out_global_efficiency').tolist(), out_global_efficiency, 3)

    def test_wu(self):
        A = np.array([[0.7577,    0.7060,    0.8235,    0.4387,    0.4898],
                      [0.7431,    0.0318,    0.6948,    0.3816,    0.4456],
                      [0.3922,    0.2769,    0.3171,    0.7655,    0.6463],
                      [0.6555,    0.0462,    0.9502,    0.7952,    0.7094],
                      [0.1712,    0.0971,    0.0344,    0.1869,    0.7547]])
        settings = GraphSettings.get_wu()
        graph = GraphFactory.get_graph(A, settings)
        global_efficiency = [0.7135, 0.6011, 0.8195, 0.7147, 0.6028]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureGlobalEfficiency,
                                       'global_efficiency').tolist(), global_efficiency, 4)

if __name__ == '__main__':
    unittest.main()
