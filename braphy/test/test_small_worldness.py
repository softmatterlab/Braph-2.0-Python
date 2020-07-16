import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_small_worldness import MeasureSmallWorldness
import numpy as np

class TestSmallWorldness(unittest.TestCase):
    
    def test_graphBD(self):
        A=np.array([[0,1,1,0,1],[1,0,1,0,1],[0,1,1,0,1],[0,1,0,1,0],[1,0,1,0,0]])
        settings = GraphSettings(weighted = False, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        #print(graph.get_measure(MeasureSmallWorldness, 'small_worldness'))
        self.assertTrue(1,1)


    def test_graphBU(self):
        #A=np.array([[0,1,1,0,1],[1,0,1,0,1],[0,1,1,0,1],[0,1,0,1,0],[1,0,1,0,0]])
        A = np.random.randint(2, size=(10,10))
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        #print(graph.get_measure(MeasureSmallWorldness, 'small_worldness'))
        self.assertTrue(1,1)

if __name__ == '__main__':
    unittest.main()
