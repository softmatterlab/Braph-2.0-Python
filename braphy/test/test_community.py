import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_community_structure import MeasureCommunityStructure
from braphy.test.test_utility import TestUtility
import numpy as np

class TestCommunity(TestUtility):
    def test_bd(self):
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        settings = GraphSettings(weighted = False, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        community = graph.get_measure(MeasureCommunityStructure, 'community_structure')
        self.assertCategorizationEqual(community, [0, 0, 0, 1])
        self.assertAlmostEqual(graph.get_measure(MeasureCommunityStructure, 'modularity'), 0.0)

    def test_bu(self):
        A = np.array([[0, 1, 1, 0, 1, 1],
                      [1, 0, 0, 0, 1, 1],
                      [1, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [1, 1, 0, 1, 1, 0],
                      [0, 0, 1, 1, 0, 0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        community = graph.get_measure(MeasureCommunityStructure, 'community_structure')
        self.assertCategorizationEqual(community, [0,0,1,1,0,1])
        self.assertAlmostEqual(graph.get_measure(MeasureCommunityStructure, 'modularity'), 0.1)

    def test_wd(self):
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = True, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        community = graph.get_measure(MeasureCommunityStructure, 'community_structure')
        self.assertCategorizationEqual(community, [0,0,0,0,1,1,1,1])
        self.assertAlmostEqual(graph.get_measure(MeasureCommunityStructure, 'modularity'), 0.3875, 4)

    def test_wu(self):
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings(weighted = True, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        community = graph.get_measure(MeasureCommunityStructure, 'community_structure')
        self.assertCategorizationEqual(community, [0,0,0,0,1,1,1,1])
        self.assertAlmostEqual(graph.get_measure(MeasureCommunityStructure, 'modularity'), 0.3806, 4)

if __name__ == '__main__':
    unittest.main()
