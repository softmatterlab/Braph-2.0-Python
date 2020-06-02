import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.test.test_utility import TestUtility
import numpy as np

class TestRandomGraphBU(unittest.TestCase):
    def test_graph(self):
        A = np.array([[0,0.5,0,0.3],[0.7,0,0.1,0],[0,0,0,0.1],[0,0,0,0]])
        settings = GraphSettings.get_wd()
        graph = GraphFactory.get_graph(A, settings)
        random = graph.get_random_graph(number_of_weights=1)
        self.assertTrue(random.shape == A.shape)
        #more tests?

if __name__ == '__main__':
    unittest.main()