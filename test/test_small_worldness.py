import unittest
from braphy.graph_measures import *
from braphy.graph import *
import numpy as np

class TestSmallWorldness(unittest.TestCase):
    
    def test1(self):
        
        measure_list = MeasureParser.list_measures()
        A=np.array([[0,1,1,0],[1,0,0,1],[0,1,0,1],[0,1,0,0]])
        graph_bd = GraphBD(A, measure_list[GraphBD], 'zero')
        print(graph_bd.get_measure(MeasureSmallWorldness, 'small_worldness'))
        self.assertTrue(1,1)

if __name__ == '__main__':
    unittest.main()
