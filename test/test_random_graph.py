import unittest
from braphy.graph import *
from braphy.graph_measures.measure_parser import MeasureParser
from braphy.graph_measures.measure_path_length import MeasurePathLength
import numpy as np

class TestRandomGraph(unittest.TestCase):
    def test_bu(self):
        measure_list = MeasureParser.list_measures()
        A=np.array([[0,1,1,0],[1,0,0,1],[0,1,0,1],[0,1,0,0]])
        graph = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        random = graph.get_random_graph()
        self.assertTrue(np.array_equal(random.A, np.array([[0,1,1,0],
                                                           [1,0,1,1],
                                                           [1,1,0,1],
                                                           [0,1,1,0]])))

    def test_bd(self):
        measure_list = MeasureParser.list_measures()
        A=np.array([[0,1,1,0,0],[1,0,0,1,0],[0,1,0,1,1],[0,1,0,0,1],[1,0,1,0,1]])
        graph = GraphBD(A, measure_list[GraphBD])
        random = graph.get_random_graph()
        self.assertTrue(random.A.shape == A.shape)
        self.assertEqual(np.sum(random.A), np.sum(A))
        char_path_length_std = 0.1259
        char_path_length_mean = 1+(1/3)
        char_path_length = random.get_measure(MeasurePathLength, 'char_path_length')
        distance = pow(char_path_length-char_path_length_mean,2)/char_path_length_std
        self.assertLess(distance, 0.35)

    def test_wd1(self):
        measure_list = MeasureParser.list_measures()
        A=np.array([[0.,1.,1.,0.5,0.],
                    [1.,0.,0.,1.,0.],
                    [0.,1.,0.,1.,1.],
                    [0.,1.,0.,0.,1.],
                    [1.,0.,1.,0.5,1.]])
        graph = GraphWD(A, measure_list[GraphWD])
        random = graph.get_random_graph()
        self.assertTrue(random.A.shape == A.shape)
        self.assertEqual(np.max(random.A), 1)
        self.assertEqual(np.min(random.A), 0)

    def test_wd2(self):
        measure_list = MeasureParser.list_measures()
        A=np.array([[0.,2.,2.,0.5,0.],
                    [1.,0.,0.,1.,0.],
                    [0.,1.,0.,-1.,1.],
                    [0.,1.,0.,0.,1.],
                    [1.,0.,1.,0.5,1.]])
        graph = GraphWD(A, measure_list[GraphWD])
        random = graph.get_random_graph()
        self.assertTrue(random.A.shape == A.shape)
        self.assertEqual(np.max(random.A), 1)
        self.assertEqual(np.min(random.A), 0)

if __name__ == '__main__':
    unittest.main()
