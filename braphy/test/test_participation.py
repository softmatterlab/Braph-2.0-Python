import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.graph_measures.measure_participation import MeasureParticipation
from braphy.test.test_utility import TestUtility
import numpy as np

class TestParticipation(TestUtility):
    def test_graphBD(self):
        A = np.array([[0, 1, 0, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [1, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)
        participation = [0, 0.5, 0.5, 0.5, 0, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureParticipation, 'participation'),
                                       participation)

    def test_graphBD_2(self):
        A = np.array([[0, 1, 0],
                      [1, 0, 1],
                      [1, 1, 0]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)
        participation = [0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureParticipation, 'participation'),
                                       participation)

    def test_graphBU(self):
        A = np.array([[0, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings.get_bu()
        graph = GraphFactory.get_graph(A, settings)
        participation = [0, 0.4444, 0.3750, 0.4444, 0.4800, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureParticipation, 'participation'),
                                       participation, places = 4)

    def test_graphWU(self):
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings.get_wu()
        graph = GraphFactory.get_graph(A, settings)
        participation = [0, 0.2449, 0.2449, 0.2449, 0.48, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureParticipation, 'participation'),
                                       participation, places = 4)

    def test_graphWD(self):
        A = np.array([[0, 0.1, 0.2, 0.1, 0, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0.2, 0, 0, 0],
                      [0, 0, 0.5, 0, 0.1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0.1, 0.5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0.2],
                      [0, 0, 0, 0, 0, 0, 0, 0.8],
                      [0, 0, 0, 0, 0, 0, 0, 0]])
        settings = GraphSettings.get_wd()
        graph = GraphFactory.get_graph(A, settings)
        participation = [0, 0.2778, 0, 0.2778, 0, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureParticipation, 'participation'),
                                       participation, places = 4)

if __name__ == '__main__':
    unittest.main()
