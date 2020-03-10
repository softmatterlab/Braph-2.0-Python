import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_z_score import MeasureZScore
from braphy.test.test_utility import TestUtility
import numpy as np

class TestZScore(TestUtility):
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
        z_score = [0.8660, -0.8660, 0.8660, -0.8660, 0, 0, 0, 0]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureZScore, 'z_score'), z_score, places = 4)

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
        z_score = [0.8660, -0.8660, 0.8660, -0.8660, 0, 0, 0, 0]
        in_z_score = [1.5, -0.5, -0.5, -0.5, 1.2247, 0, 0, -1.2247]
        out_z_score = [-0.5, -0.5, 1.5, -0.5, -1.2247, 0, 0, 1.2247]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureZScore, 'z_score'), z_score, places = 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureZScore, 'in_z_score'), in_z_score, places = 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureZScore, 'out_z_score'), out_z_score, places = 4)

    def test_graphWD(self):
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, 75],
                      [13, 0.0, 1.2, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0005, 0.5],
                      [1, 0.0, 345, 8.7, 2]])
        settings = GraphSettings.get_wd()
        graph = GraphFactory.get_graph(A, settings)
        z_score = [-1.1510, 0.6553, 0, 0.4957, 0]
        in_z_score = [-1.0792, 0.1840, -0.7071, 0.8952, 0.7071]
        out_z_score = [-0.0933, 1.0434, 0.7071, -0.9501, -0.7071]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureZScore, 'z_score'), z_score, places = 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureZScore, 'in_z_score'), in_z_score, places = 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureZScore, 'out_z_score'), out_z_score, places = 4)

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
        z_score = [-0.8660, -0.2887, 1.4434, -0.2887, -0.4549, -1.1371, 1.1371, 0.4549]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasureZScore, 'z_score'), z_score, places = 4)

if __name__ == '__main__':
    unittest.main()
