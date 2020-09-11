import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_community_structure import MeasureCommunityStructure
import numpy as np

class TestModularity(unittest.TestCase):
    def test_modularity_bu_1(self):
        A = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        self.assertAlmostEqual(graph.get_measure(MeasureCommunityStructure, 'modularity'), 0, places = 4)

    def test_modularity_bu_2(self):
        A = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        self.assertAlmostEqual(graph.get_measure(MeasureCommunityStructure, 'modularity'), 5.5511e-17,
                               places = 4)

    def test_modularity_wu(self):
        A = np.array([[0, 999999, 999999, 0, 0, 0],
                      [999999, 0, 999999, 0, 0, 0],
                      [999999, 999999, 0, 1, 0, 0],
                      [0, 0, 1, 0, 999999, 999999],
                      [0, 0, 0, 999999, 0, 999999],
                      [0, 0, 0, 999999, 999999, 0]])
        settings = GraphSettings(weighted = True, directed = False, rule_standardize = 'range')
        graph = GraphFactory.get_graph(A, settings)
        self.assertAlmostEqual(graph.get_measure(MeasureCommunityStructure, 'modularity'), 0.5, places = 4)

if __name__ == '__main__':
    unittest.main()
