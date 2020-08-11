import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_path_length import MeasurePathLength
import numpy as np

class TestRandomGraph(unittest.TestCase):
    def test_bu(self):
        A = np.array([[0,1,1,0],[1,0,0,1],[0,1,0,1],[0,1,0,0]])
        settings = GraphSettings(weighted = False, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        random = graph.get_random_graph()
        self.assertTrue(np.array_equal(random, np.array([[0,1,1,0],
                                                           [1,0,1,1],
                                                           [1,1,0,1],
                                                           [0,1,1,0]])))

    def test_bd(self):
        A = np.array([[0,1,1,0,0],[1,0,0,1,0],[0,1,0,1,1],[0,1,0,0,1],[1,0,1,0,1]])
        settings = GraphSettings(weighted = False, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        random = graph.get_random_graph()
        self.assertTrue(random.shape == A.shape)
        self.assertEqual(np.sum(random), np.sum(A))
        char_path_length_std = 0.1259
        char_path_length_mean = 1+(1/3)
        random_graph = GraphFactory.get_graph(random, settings)
        char_path_length = random_graph.get_measure(MeasurePathLength, 'char_path_length')
        distance = pow(char_path_length-char_path_length_mean,2)/char_path_length_std
        self.assertLess(distance, 0.35)

    def test_wd1(self):
        A = np.array([[0.,1.,1.,0.5,0.],
                      [1.,0.,0.,1.,0.],
                      [0.,1.,0.,1.,1.],
                      [0.,1.,0.,0.,1.],
                      [1.,0.,1.,0.5,1.]])
        settings = GraphSettings(weighted = True, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        random = graph.get_random_graph()
        self.assertTrue(random.shape == A.shape)

    def test_wd2(self):
        A = np.array([[0.,2.,2.,0.5,0.],
                      [1.,0.,0.,1.,0.],
                      [0.,1.,0.,-1.,1.],
                      [0.,1.,0.,0.,1.],
                      [1.,0.,1.,0.5,1.]])
        settings = GraphSettings(weighted = True, directed = True)
        graph = GraphFactory.get_graph(A, settings)
        random = graph.get_random_graph()
        self.assertTrue(random.shape == A.shape)

    def test_wu(self):
        A = np.array([[0,1,1,0],[1,0,0,1],[0,1,0,1],[0,1,0,0]])
        settings = GraphSettings(weighted = True, directed = False)
        graph = GraphFactory.get_graph(A, settings)
        random = graph.get_random_graph()
        self.assertTrue(np.array_equal(random, np.array([[0,1,1,0],
                                                           [1,0,1,1],
                                                           [1,1,0,1],
                                                           [0,1,1,0]])))

if __name__ == '__main__':
    unittest.main()
