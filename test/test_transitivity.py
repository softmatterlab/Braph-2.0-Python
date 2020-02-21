import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_transitivity import MeasureTransitivity
from braphy.graph import *
import numpy as np

class TestTransitivity(unittest.TestCase):
    def test_bd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0],
                      [1, 0, 1, 0],
                      [1, 1, 0, 1],
                      [0, 0, 1, 0]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        MeasureTransitivity.compute_measure(graph)
        self.assertAlmostEqual(graph.measure_dict[MeasureTransitivity]['transitivity'], 0.45)

    def test_bu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0],
                      [1, 0, 1, 0],
                      [1, 1, 0, 1],
                      [0, 0, 1, 0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        MeasureTransitivity.compute_measure(graph)
        self.assertAlmostEqual(graph.measure_dict[MeasureTransitivity]['transitivity'], 0.6)

    def test_wd(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0],
                      [1, 0, 1, 0],
                      [1, 1, 0, 1],
                      [0, 0, 1, 0]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        MeasureTransitivity.compute_measure(graph)
        self.assertAlmostEqual(graph.measure_dict[MeasureTransitivity]['transitivity'], 0.225)

    def test_wu(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 0],
                      [1, 0, 1, 0],
                      [1, 1, 0, 1],
                      [0, 0, 1, 0]])
        graph = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        MeasureTransitivity.compute_measure(graph)
        self.assertAlmostEqual(graph.measure_dict[MeasureTransitivity]['transitivity'], 0.9)

if __name__ == '__main__':
    unittest.main()
