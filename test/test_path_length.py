import unittest
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_path_length import MeasurePathLength
from test.test_utility import TestUtility
from braphy.graph import *
import numpy as np

class TestPathLength(TestUtility):

    def test_graphBD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, 0, 1, 1, 1],
                      [0, 1, 1, 0, 1],
                      [1, 0, 1, 1, 1],
                      [0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 1]])
        graph = GraphBD(A, measure_list[GraphBD], 'zero')
        path_length = [1.458333, 1.5833, 1.1250, np.nan, 1.2500]
        in_path_length = [1.6667, 1.6667, 1.0, 1.5, 1.0]
        out_path_length = [1.25, 1.5, 1.25, np.nan, 1.5]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasurePathLength, 'path_length'),
                                       path_length, places = 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasurePathLength, 'in_path_length'),
                                       in_path_length, places = 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasurePathLength, 'out_path_length'),
                                       out_path_length, places = 4)

    def test_graphBU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[1, 0, 1, 1, 1],
                      [0, 1, 1, 0, 1],
                      [1, 0, 1, 1, 1],
                      [0, 0, 0, 0, 0],
                      [0, 1, 1, 0, 1]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        true_path_length = [1.25, 1.5, 1.0, 1.5, 1.25]
        self.assertSequenceEqual(graph.get_measure(MeasurePathLength, 'path_length').tolist(),
                                 true_path_length)

    def test_graphWD(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, 75],
                      [13, 0.0, 1.2, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0005, 0.5],
                      [1, 0.0, 345, 8.7, 2]])
        graph = GraphWD(A, measure_list[GraphWD], 'zero')
        path_length = [80.3610, 52.8584, 58.3262, 62.2139, 52.8584]
        in_path_length = [37.2357, 84.0684, 42.4364, 74.6411, 68.2363]
        out_path_length = [123.4864, 21.6484, 74.2159, 49.7867, 37.4805]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasurePathLength, 'path_length'),
                                       path_length, places = 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasurePathLength, 'in_path_length'),
                                       in_path_length, places = 4)
        self.assertSequenceAlmostEqual(graph.get_measure(MeasurePathLength, 'out_path_length'),
                                       out_path_length, places = 4)

    def test_graphWU(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[3.2, 3.14, 2.7, 0.01, 0.0],
                      [3.2, 2.7, 3.14, 6.7, 75],
                      [13, 0.0, 1.2, 5.7, 0.01],
                      [5.5, 8.2, 0.3, 0.0005, 0.5],
                      [1, 0.0, 345, 8.7, 2]])
        graph = GraphWU(A, measure_list[GraphWU], 'zero', 'max')
        path_length = [37.2357, 21.1029, 18.4484, 46.2777, 18.1984]
        self.assertSequenceAlmostEqual(graph.get_measure(MeasurePathLength, 'path_length'),
                                       path_length, places = 4)

if __name__ == '__main__':
    unittest.main()
