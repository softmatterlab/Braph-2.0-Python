import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_degree import MeasureDegree
import numpy as np

class TestDegree(unittest.TestCase):
    def test_graphBD(self):
        A = np.array([[0, 1, 1, 1, 0, 1, 0, 0, 0, 1], [0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
                      [0, 0, 0, 1, 0, 0, 0, 1, 1, 0], [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
                      [1, 1, 0, 0, 1, 1, 0, 1, 1, 1], [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                      [1, 1, 0, 0, 1, 1, 0, 1, 1, 1], [0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
                      [0, 1, 1, 0, 1, 1, 1, 0, 1, 0], [1, 0, 1, 0, 1, 1, 0, 1, 1, 0]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceEqual(graph.get_measure(MeasureDegree, 'degree').tolist(),
                                 [10, 7, 8, 10, 12, 11, 9, 10, 12, 9])
        self.assertSequenceEqual(graph.get_measure(MeasureDegree, 'in_degree').tolist(),
                                 [5, 5, 5, 4, 6, 7, 2, 5, 7, 3])
        self.assertSequenceEqual(graph.get_measure(MeasureDegree, 'out_degree').tolist(),
                                 [5, 2, 3, 6, 6, 4, 7, 5, 5, 6])
        self.assertEqual(graph.get_measure(MeasureDegree, 'avg_degree'), 9.8)
        self.assertEqual(graph.get_measure(MeasureDegree, 'avg_in_degree'), 4.9)
        self.assertEqual(graph.get_measure(MeasureDegree, 'avg_out_degree'), 4.9)

    def test_graphBU(self):
        A = np.array([[0, 1, 1, 1, 0, 1, 0, 0, 0, 1], [0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
                      [0, 0, 0, 1, 0, 0, 0, 1, 1, 0], [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
                      [1, 1, 0, 0, 1, 1, 0, 1, 1, 1], [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                      [1, 1, 0, 0, 1, 1, 0, 1, 1, 1], [0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
                      [0, 1, 1, 0, 1, 1, 1, 0, 1, 0], [1, 0, 1, 0, 1, 1, 0, 1, 1, 0]])
        settings = GraphSettings.get_bu()
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceEqual(graph.get_measure(MeasureDegree, 'degree').tolist(),
                                 [7, 6, 6, 7, 8, 9, 8, 8, 8, 7])
        self.assertEqual(graph.get_measure(MeasureDegree, 'avg_degree'), 7.4)

    def test_graphWD(self):
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, -75],
                      [13, 0.0, 1.2, 5.7, -0.01],
                      [5.5, 8.2, 0.3, 0.0005, -0.5],
                      [1, 0.0, 345, 8.7, -2]])
        settings = GraphSettings.get_wd(rule_semipositivize = 'abs')
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceEqual(graph.get_measure(MeasureDegree, 'degree').tolist(),
                                 [7, 6, 7, 8, 6])
        self.assertSequenceEqual(graph.get_measure(MeasureDegree, 'in_degree').tolist(),
                                 [4, 2, 4, 4, 3])
        self.assertSequenceEqual(graph.get_measure(MeasureDegree, 'out_degree').tolist(),
                                 [3, 4, 3, 4, 3])
        self.assertEqual(graph.get_measure(MeasureDegree, 'avg_degree'), 6.8)
        self.assertEqual(graph.get_measure(MeasureDegree, 'avg_in_degree'), 3.4)
        self.assertEqual(graph.get_measure(MeasureDegree, 'avg_out_degree'), 3.4)

    def test_graphWU(self):
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, -75],
                      [13, 0.0, 1.2, 5.7, -0.01],
                      [5.5, 8.2, 0.3, 0.0005, -0.5],
                      [1, 0.0, 345, 8.7, -2]])
        settings = GraphSettings.get_wu()
        graph = GraphFactory.get_graph(A, settings)
        self.assertSequenceEqual(graph.get_measure(MeasureDegree, 'degree').tolist(),
                                 [4, 3, 4, 4, 3])
        self.assertEqual(graph.get_measure(MeasureDegree, 'avg_degree'), 3.6)

if __name__ == '__main__':
    unittest.main()
