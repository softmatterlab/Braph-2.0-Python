import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.test.test_utility import TestUtility
import numpy as np

class TestRandomGraphBD(unittest.TestCase):
    def test_graph(self):
        A = np.array([[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)
        random = graph.get_random_graph()
        self.assertTrue(random.shape == A.shape)
        self.assertEqual(np.sum(random), np.sum(A))

if __name__ == '__main__':
    unittest.main()