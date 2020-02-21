import unittest
from braphy.graph.community_algorithms import CommunityAlgorithms
from braphy.graph_measures import MeasureParser
from braphy.graph_measures.measure_modularity import MeasureModularity
from braphy.graph import *
from test.test_utility import TestUtility
import numpy as np

class TestCommunity(TestUtility):
    def test_bd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        community = graph.community_structure
        self.assertCategorizationEqual(community, [0, 0, 0, 1])
        self.assertAlmostEqual(graph.get_measure(MeasureModularity, 'modularity'), 0.0)

    def test_bu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0, 1, 1],
                      [1, 0, 0, 0, 1, 1],
                      [1, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [1, 1, 0, 1, 1, 0],
                      [0, 0, 1, 1, 0, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero')
        community = graph.community_structure
        self.assertCategorizationEqual(community, [0,0,1,1,0,1])
        self.assertAlmostEqual(graph.get_measure(MeasureModularity, 'modularity'), 0.1)

    def test_wd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        community = graph.community_structure
        self.assertCategorizationEqual(community, [0,0,0,0,1,1,1,1])
        self.assertAlmostEqual(graph.get_measure(MeasureModularity, 'modularity'), 0.3875, places = 4)

    def test_wu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph = GraphWU(A, measure_list[GraphWU], 'zero')
        community = graph.community_structure
        self.assertCategorizationEqual(community, [0,0,0,0,1,1,1,1])
        self.assertAlmostEqual(graph.get_measure(MeasureModularity, 'modularity'), 0.3806, places = 4)

if __name__ == '__main__':
    unittest.main()
