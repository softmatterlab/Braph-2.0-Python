import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_local_efficiency import MeasureLocalEfficiency
from braphy.test.test_utility import TestUtility
import numpy as np

class TestLocalEfficiency(TestUtility):
    def test_bd(self):
        A = np.array([[0, 1, 0, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [1, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = False, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        local_efficiency = [0.3333, 0.3333, 0.3750, 0.3333, 0.1000, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureLocalEfficiency,
                                       'in_local_efficiency').tolist(), local_efficiency, 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureLocalEfficiency,
                                       'out_local_efficiency').tolist(), local_efficiency, 4)

    def test_bu(self):
        A = np.array([[0, 1, 0, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [1, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        local_efficiency = [0.8333, 0.8333, 0.8333, 0.8333, 0.2500, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureLocalEfficiency,
                                       'local_efficiency').tolist(), local_efficiency, 4)

    def test_wd(self):
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0.2, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = True, directed = True, rule_standardize = 'range')
        graph = GraphFactory.get_graph(A, settings)
        local_efficiency = [] # new version in matlab, waiting for implementation
        #self.assertSequenceAlmostEqual(graph.get_measure(MeasureLocalEfficiency,
        #                               'in_local_efficiency').tolist(), local_efficiency, 4)
        #self.assertSequenceAlmostEqual(graph.get_measure(MeasureLocalEfficiency,
        #                               'out_local_efficiency').tolist(), local_efficiency, 4)

    def test_wu(self):
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0.2, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = True, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        local_efficiency = [0.4167, 0.1667, 0.0833, 0.1667, 0.1250, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureLocalEfficiency,
                                       'local_efficiency').tolist(), local_efficiency, 4)

if __name__ == '__main__':
    unittest.main()
