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
    
    def test_bd(self):
        measure_list = MeasureParser.list_measures()
        A=np.array([[0,1,1,0,0],[1,0,0,1,0],[0,1,0,1,1],[0,1,0,0,1],[1,0,1,0,1]])
        graph = GraphBD(A, measure_list[GraphBD])
        random = graph.get_random_graph()
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
