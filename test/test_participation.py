import unittest
from braphy.graph_measures import *
from braphy.graph import *
from test.test_utility import TestUtility
import numpy as np

class TestParticipation(TestUtility):
    def test_graphBD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 0, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [1, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph_bd = GraphBD(A, measure_list[GraphBD])
        participation = [0, 0.5, 0.5, 0.5, 0, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph_bd.get_measure(MeasureParticipation, 'participation'),
                                       participation)

    def test_graphBD_2(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 0],
                      [1, 0, 1],
                      [1, 1, 0]])
        graph_bd = GraphBD(A, measure_list[GraphBD])
        participation = [0, 0, 0]
        self.assertSequenceAlmostEqual(graph_bd.get_measure(MeasureParticipation, 'participation'),
                                       participation)

    def test_graphBU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph_bu = GraphBU(A, measure_list[GraphBU])
        participation = [0, 0.4444, 0.3750, 0.4444, 0.4800, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph_bu.get_measure(MeasureParticipation, 'participation'),
                                       participation, places = 4)

    def test_graphWU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph_wu = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        participation = [0, 0.2449, 0.2449, 0.2449, 0.48, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph_wu.get_measure(MeasureParticipation, 'participation'),
                                       participation, places = 4)

    def test_graphWD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        graph_wd = GraphWD(A, measure_list[GraphWD])
        participation = [0, 0.2778, 0, 0.2778, 0, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph_wd.get_measure(MeasureParticipation, 'participation'),
                                       participation, places = 4)

if __name__ == '__main__':
    unittest.main()
