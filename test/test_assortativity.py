import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_assortativity import MeasureAssortativity
from braphy.graph import *
import numpy as np

class TestAssortativity(unittest.TestCase):
    def test_bd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        self.assertEqual(graph.get_measure(MeasureAssortativity, 'assortativity_out_in'), -1)
        self.assertEqual(graph.get_measure(MeasureAssortativity, 'assortativity_in_out'), -1)
        self.assertEqual(graph.get_measure(MeasureAssortativity, 'assortativity_out_out'), -1)
        self.assertEqual(graph.get_measure(MeasureAssortativity, 'assortativity_in_in'), -1)

    def test_bd_2(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
                      [0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
                      [0, 0, 0, 1, 0, 0, 0, 1, 1, 0],
                      [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
                      [1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
                      [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                      [1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
                      [0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
                      [0, 1, 1, 0, 1, 1, 1, 0, 1, 0],
                      [1, 0, 1, 0, 1, 1, 0, 1, 1, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        self.assertAlmostEqual(graph.get_measure(MeasureAssortativity, 'assortativity_out_in'), -0.0840, places = 4)
        self.assertAlmostEqual(graph.get_measure(MeasureAssortativity, 'assortativity_in_out'), -0.0420, places = 4)
        self.assertAlmostEqual(graph.get_measure(MeasureAssortativity, 'assortativity_out_out'), -0.0810, places = 4)
        self.assertAlmostEqual(graph.get_measure(MeasureAssortativity, 'assortativity_in_in'), -0.1476, places = 4)

    def test_bu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
                      [0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
                      [0, 0, 0, 1, 0, 0, 0, 1, 1, 0],
                      [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
                      [1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
                      [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                      [1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
                      [0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
                      [0, 1, 1, 0, 1, 1, 1, 0, 1, 0],
                      [1, 0, 1, 0, 1, 1, 0, 1, 1, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        self.assertAlmostEqual(graph.get_measure(MeasureAssortativity, 'assortativity'), -0.1903485)

    def test_wd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, -75],
                      [13, 0.0, 1.2, 5.7, -0.01],
                      [5.5, 8.2, 0.3, 0.0005, -0.5],
                      [1, 0.0, 345, 8.7, -2]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        self.assertAlmostEqual(graph.get_measure(MeasureAssortativity, 'assortativity_out_in'), 0.0451, places = 4)
        self.assertAlmostEqual(graph.get_measure(MeasureAssortativity, 'assortativity_in_out'), -0.0973, places = 4)
        self.assertAlmostEqual(graph.get_measure(MeasureAssortativity, 'assortativity_out_out'), -0.1191, places = 4)
        self.assertAlmostEqual(graph.get_measure(MeasureAssortativity, 'assortativity_in_in'), -0.2731, places = 4)

    def test_wu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, -75],
                      [13, 0.0, 1.2, 5.7, -0.01],
                      [5.5, 8.2, 0.3, 0.0005, -0.5],
                      [1, 0.0, 345, 8.7, -2]])
        graph = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        self.assertAlmostEqual(graph.get_measure(MeasureAssortativity, 'assortativity'), -0.166126077)

if __name__ == '__main__':
    unittest.main()
