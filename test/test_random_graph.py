import unittest
from braphy.graph import *
from braphy.graph_measures.measure_parser import MeasureParser
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

    def test_wd(self):
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

    '''
    def test(self):
        measure_list = MeasureParser.list_measures()
        A = np.array([[0, 1, 1, 1, 0, 1, 0, 0, 0, 1], [0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
                      [0, 0, 0, 1, 0, 0, 0, 1, 1, 0], [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
                      [1, 1, 0, 0, 1, 1, 0, 1, 1, 1], [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                      [1, 1, 0, 0, 1, 1, 0, 1, 1, 1], [0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
                      [0, 1, 1, 0, 1, 1, 1, 0, 1, 0], [1, 0, 1, 0, 1, 1, 0, 1, 1, 0]])
        graph_bu = GraphBU(A, measure_list[GraphBU], 'zero', 'max')
        random = graph_bu.get_random_graph()
        print(random)
    '''
if __name__ == '__main__':
    unittest.main()
