import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.test.test_utility import TestUtility
from braphy.graph.measures.measure_path_length import MeasurePathLength
from braphy.graph.measures.measure_transitivity import MeasureTransitivity
from braphy.graph.measures.measure_cluster import MeasureCluster
from braphy.graph.graphs.graphBU import GraphBU
import numpy as np
from matplotlib import pyplot as plt
import sys
from braphy.utility.helper_functions import *

class TestRandomGraphSmallBU(unittest.TestCase):
    def test_graph1(self):
        A = small_world_graph(6,2,0.5)
        print(A)
        '''np.set_printoptions(threshold=sys.maxsize)
        print(A)
        settings = GraphSettings.get_bu()
        settings.value_binary = 1
        graph = GraphFactory.get_graph(A, settings)

        char_path_length = graph.get_measure(MeasurePathLength, 'char_path_length')
        transitivity = graph.get_measure(MeasureTransitivity, 'transitivity')
        avg_cluster = graph.get_measure(MeasureCluster, 'avg_cluster')
        print('')
        print('Case 1, with small world BU of size: ', A.shape)
        print('Char. path length: ', char_path_length)
        print('Transitivity: ', transitivity)
        print('Avg. cluster: ', avg_cluster)

        random_ = graph.get_random_graph()
        random = GraphBU(random_, graph.settings)
        self.assertTrue(random.A.shape == graph.A.shape)
        self.assertEqual(np.sum(random.A), np.sum(graph.A))

        case_1_random_measures = np.zeros((3, 1000))
        for i in range(0,1000):
            random = graph.get_random_graph()
            random = GraphBU(random, graph.settings)

            char_path_length_random = random.get_measure(MeasurePathLength, 'char_path_length')
            case_1_random_measures[0,i] = char_path_length_random

            transitivity_random = random.get_measure(MeasureTransitivity, 'transitivity')
            case_1_random_measures[1,i] = transitivity_random

            avg_cluster_random = random.get_measure(MeasureCluster, 'avg_cluster')
            case_1_random_measures[2,i] = avg_cluster_random

        fig, axs = plt.subplots(3)
        fig.suptitle('Test case 1: input small world BU, graph dim=' + str(A.shape))
        axs[0].hist(case_1_random_measures[0,:], bins='auto')
        axs[0].set_title('Char. path length of input graph=' + str('%.3f'%(char_path_length)))
        axs[0].set_xlabel('Char. path length of random graphs')
        axs[1].hist(case_1_random_measures[1,:], bins='auto')
        axs[1].set_title('Transitivity of input graph=' + str('%.3f'%(transitivity)))
        axs[1].set_xlabel('Transitivity of random graphs')
        axs[2].hist(case_1_random_measures[2,:], bins='auto')
        axs[2].set_title('Avg. cluster of input graph=' + str('%.3f'%(avg_cluster)))
        axs[2].set_xlabel('Avg. cluster of random graphs')
        fig.tight_layout(pad=3.0)
        plt.show(block=False)

    def test_graph2(self):
        #beta = 1 as below gives a random graph
        A = small_world_graph(20,6,1)
        np.set_printoptions(threshold=sys.maxsize)
        print(A)
        settings = GraphSettings.get_bu()
        settings.value_binary = 1
        graph = GraphFactory.get_graph(A, settings)

        char_path_length = graph.get_measure(MeasurePathLength, 'char_path_length')
        transitivity = graph.get_measure(MeasureTransitivity, 'transitivity')
        avg_cluster = graph.get_measure(MeasureCluster, 'avg_cluster')
        print('')
        print('Case 2, with small world BU of size: ', A.shape)
        print('Char. path length: ', char_path_length)
        print('Transitivity: ', transitivity)
        print('Avg. cluster: ', avg_cluster)

        random_ = graph.get_random_graph()
        random = GraphBU(random_, graph.settings)
        self.assertTrue(random.A.shape == graph.A.shape)
        self.assertEqual(np.sum(random.A), np.sum(graph.A))

        case_2_random_measures = np.zeros((3, 1000))
        for i in range(0,1000):
            random = graph.get_random_graph()
            random = GraphBU(random, graph.settings)

            char_path_length_random = random.get_measure(MeasurePathLength, 'char_path_length')
            case_2_random_measures[0,i] = char_path_length_random

            transitivity_random = random.get_measure(MeasureTransitivity, 'transitivity')
            case_2_random_measures[1,i] = transitivity_random

            avg_cluster_random = random.get_measure(MeasureCluster, 'avg_cluster')
            case_2_random_measures[2,i] = avg_cluster_random

        fig, axs = plt.subplots(3)
        fig.suptitle('Test case 1: input small world BU, graph dim=' + str(A.shape))
        axs[0].hist(case_2_random_measures[0,:], bins='auto')
        axs[0].set_title('Char. path length of input graph=' + str('%.3f'%(char_path_length)))
        axs[0].set_xlabel('Char. path length of random graphs')
        axs[1].hist(case_2_random_measures[1,:], bins='auto')
        axs[1].set_title('Transitivity of input graph=' + str('%.3f'%(transitivity)))
        axs[1].set_xlabel('Transitivity of random graphs')
        axs[2].hist(case_2_random_measures[2,:], bins='auto')
        axs[2].set_title('Avg. cluster of input graph=' + str('%.3f'%(avg_cluster)))
        axs[2].set_xlabel('Avg. cluster of random graphs')
        fig.tight_layout(pad=3.0)
        plt.show()'''

if __name__ == '__main__':
    unittest.main()
