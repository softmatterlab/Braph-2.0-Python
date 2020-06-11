import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.test.test_utility import TestUtility
from braphy.graph.measures.measure_path_length import MeasurePathLength
from braphy.graph.measures.measure_transitivity import MeasureTransitivity
from braphy.graph.measures.measure_cluster import MeasureCluster
from braphy.graph.graphs.graphBD import GraphBD
import numpy as np

class TestRandomGraphBD(unittest.TestCase):
    def test_graph1(self):
        A = np.array([[0,1,0,1], [0,0,1,0], [0,0,0,0], [0,1,1,0]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)
        random = graph.get_random_graph()
        random = GraphBD(random, graph.settings)
        self.assertTrue(random.A.shape == A.shape)
        self.assertEqual(np.sum(random.A), np.sum(A))
        char_path_length = graph.get_measure(MeasurePathLength, 'char_path_length')
        char_path_length_random = random.get_measure(MeasurePathLength, 'char_path_length')
        print(char_path_length)
        print(char_path_length_random) #these do not equal


    def test_graph2(self):
        A = np.array([[0,0,0,1,0,0,0,0,0,0], [1,0,0,0,1,0,0,0,0,0], [1,0,0,0,1,0,0,0,0,0], 
                      [0,1,1,0,0,0,0,0,0,0], [0,0,0,1,0,0,0,0,1,1], [0,0,0,0,0,0,1,0,0,1], 
                      [0,0,0,0,0,0,0,1,0,0], [0,0,0,0,0,1,1,0,0,0], [0,0,0,0,0,0,0,0,0,0], 
                      [0,0,0,0,1,0,0,0,0,0]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)
        random = graph.get_random_graph()
        random = GraphBD(random, graph.settings)
        self.assertTrue(random.A.shape == A.shape)
        self.assertEqual(np.sum(random.A), np.sum(A))
        char_path_length = graph.get_measure(MeasurePathLength, 'char_path_length')
        char_path_length_random = random.get_measure(MeasurePathLength, 'char_path_length')
        print(char_path_length)
        print(char_path_length_random) #these do not equal
        transitivity = graph.get_measure(MeasureTransitivity, 'transitivity').tolist()
        transitivity_random = random.get_measure(MeasureTransitivity, 'transitivity').tolist()
        print(transitivity)
        print(transitivity_random) #these do not equal
        avg_cluster = graph.get_measure(MeasureCluster, 'avg_cluster').tolist()
        avg_cluster_random = random.get_measure(MeasureCluster, 'avg_cluster').tolist()
        print(avg_cluster)
        print(avg_cluster_random) #these do not equal


if __name__ == '__main__':
    unittest.main()