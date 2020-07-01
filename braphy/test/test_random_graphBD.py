import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.test.test_utility import TestUtility
from braphy.graph.measures.measure_path_length import MeasurePathLength
from braphy.graph.measures.measure_transitivity import MeasureTransitivity
from braphy.graph.measures.measure_cluster import MeasureCluster
from braphy.graph.graphs.graphBD import GraphBD
import numpy as np
from matplotlib import pyplot as plt

class TestRandomGraphBD(unittest.TestCase):
    def test_graph1(self):
        A = np.array([[0., 1., 0., 1.], [0., 0., 1., 0.], [0., 0., 0., 0.], [0., 1., 1., 0.]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)
        random = graph.get_random_graph()
        random = GraphBD(random, graph.settings)
        self.assertTrue(random.A.shape == A.shape)
        self.assertEqual(np.sum(random.A), np.sum(A))
        char_path_length = graph.get_measure(MeasurePathLength, 'char_path_length')
        char_path_length_random = random.get_measure(MeasurePathLength, 'char_path_length')
        print('Case 1, with BD of size: ', A.shape)
        print('Char. path length: ', char_path_length)
        print('Char. path length random: ', char_path_length_random)

    def test_graph2(self):
        A = np.array([[0., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
                      [1., 0., 0., 0., 1., 0., 0., 0., 0., 0.],
                      [1., 0., 0., 0., 1., 0., 0., 0., 0., 0.],
                      [0., 1., 1., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 1., 0., 0., 0., 0., 1., 1.],
                      [0., 0., 0., 0., 0., 0., 1., 0., 0., 1.],
                      [0., 0., 0., 0., 0., 0., 0., 1., 0., 0.],
                      [0., 0., 0., 0., 0., 1., 1., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 1., 0., 0., 0., 0., 0.]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)

        char_path_length = graph.get_measure(MeasurePathLength, 'char_path_length')
        transitivity = graph.get_measure(MeasureTransitivity, 'transitivity')
        avg_cluster = graph.get_measure(MeasureCluster, 'avg_cluster')
        print('')
        print('Case 2, with BD of size: ', A.shape)
        print('Char. path length: ', char_path_length)
        print('Transitivity: ', transitivity)
        print('Avg. cluster: ', avg_cluster)

        random = graph.get_random_graph()
        random = GraphBD(random, graph.settings)
        self.assertTrue(random.A.shape == A.shape)
        self.assertEqual(np.sum(random.A), np.sum(A))

        case_2_random_measures = np.zeros((3, 1000))
        for i in range(0,1000):
            random = graph.get_random_graph()
            random = GraphBD(random, graph.settings)

            char_path_length_random = random.get_measure(MeasurePathLength, 'char_path_length')
            case_2_random_measures[0,i] = char_path_length_random

            transitivity_random = random.get_measure(MeasureTransitivity, 'transitivity')
            case_2_random_measures[1,i] = transitivity_random

            avg_cluster_random = random.get_measure(MeasureCluster, 'avg_cluster')
            case_2_random_measures[2,i] = avg_cluster_random

        fig, axs = plt.subplots(3)
        fig.suptitle('Test case 2: input BD graph dim=' + str(A.shape))
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
        plt.show(block=False)


    def test_graph3(self):
        A = np.array([[0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 1., 0., 0., 0., 0., 0., 1., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1.],
                      [0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 1.],
                      [0., 0., 1., 0., 0., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1., 1., 1., 0., 0.],
                      [0., 0., 0., 0., 0., 1., 0., 0., 0., 1., 0., 0., 1., 0., 0., 0., 1., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 0., 0., 0., 0., 0., 0., 1., 0.],
                      [0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 1., 1., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 1., 0., 0., 0., 1., 0., 0., 0., 0., 0., 1., 1., 0., 0., 0., 0., 0.],
                      [0., 1., 0., 1., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 1., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 1., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1., 1.],
                      [0., 0., 0., 0., 0., 1., 1., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
                      [0., 0., 0., 1., 0., 0., 0., 1., 1., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)

        char_path_length = graph.get_measure(MeasurePathLength, 'char_path_length')
        transitivity = graph.get_measure(MeasureTransitivity, 'transitivity')
        avg_cluster = graph.get_measure(MeasureCluster, 'avg_cluster')
        print('')
        print('Case 3, with BD of size: ', A.shape)
        print('Char. path length: ', char_path_length)
        print('Transitivity: ', transitivity)
        print('Avg. cluster: ', avg_cluster)

        random = graph.get_random_graph()
        random = GraphBD(random, graph.settings)
        self.assertTrue(random.A.shape == A.shape)
        self.assertEqual(np.sum(random.A), np.sum(A))

        case_3_random_measures = np.zeros((3, 1000))
        for i in range(0,1000):
            random = graph.get_random_graph()
            random = GraphBD(random, graph.settings)

            char_path_length_random = random.get_measure(MeasurePathLength, 'char_path_length')
            case_3_random_measures[0,i] = char_path_length_random

            transitivity_random = random.get_measure(MeasureTransitivity, 'transitivity')
            case_3_random_measures[1,i] = transitivity_random

            avg_cluster_random = random.get_measure(MeasureCluster, 'avg_cluster')
            case_3_random_measures[2,i] = avg_cluster_random

        fig, axs = plt.subplots(3)
        fig.suptitle('Test case 3: input BD graph dim=' + str(A.shape))
        axs[0].hist(case_3_random_measures[0,:], bins='auto')
        axs[0].set_title('Char. path length of input graph=' + str('%.3f'%(char_path_length)))
        axs[0].set_xlabel('Char. path length of random graphs')
        axs[1].hist(case_3_random_measures[1,:], bins='auto')
        axs[1].set_title('Transitivity of input graph=' + str('%.3f'%(transitivity)))
        axs[1].set_xlabel('Transitivity of random graphs')
        axs[2].hist(case_3_random_measures[2,:], bins='auto')
        axs[2].set_title('Avg. cluster of input graph=' + str('%.3f'%(avg_cluster)))
        axs[2].set_xlabel('Avg. cluster of random graphs')
        fig.tight_layout(pad=3.0)
        plt.show(block=False)

    def test_graph4(self): #high in clusters, not much random connections
        A = np.array([[0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [1., 0., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 1., 0., 1., 1., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 1., 0., 1., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 1., 0., 0., 1.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 1., 1., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.],
                      [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0.]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)

        char_path_length = graph.get_measure(MeasurePathLength, 'char_path_length')
        transitivity = graph.get_measure(MeasureTransitivity, 'transitivity')
        avg_cluster = graph.get_measure(MeasureCluster, 'avg_cluster')
        print('')
        print('Case 4, with BD of size: ', A.shape)
        print('Char. path length: ', char_path_length)
        print('Transitivity: ', transitivity)
        print('Avg. cluster: ', avg_cluster)

        random = graph.get_random_graph()
        random = GraphBD(random, graph.settings)
        self.assertTrue(random.A.shape == A.shape)
        self.assertEqual(np.sum(random.A), np.sum(A))

        case_4_random_measures = np.zeros((3, 1000))
        for i in range(0,1000):
            random = graph.get_random_graph()
            random = GraphBD(random, graph.settings)

            char_path_length_random = random.get_measure(MeasurePathLength, 'char_path_length')
            case_4_random_measures[0,i] = char_path_length_random

            transitivity_random = random.get_measure(MeasureTransitivity, 'transitivity')
            case_4_random_measures[1,i] = transitivity_random

            avg_cluster_random = random.get_measure(MeasureCluster, 'avg_cluster')
            case_4_random_measures[2,i] = avg_cluster_random

        fig, axs = plt.subplots(3)
        fig.suptitle('Test case 4: input BD graph dim=' + str(A.shape))
        axs[0].hist(case_4_random_measures[0,:], bins='auto')
        axs[0].set_title('Char. path length of input graph=' + str('%.3f'%(char_path_length)))
        axs[0].set_xlabel('Char. path length of random graphs')
        axs[1].hist(case_4_random_measures[1,:], bins='auto')
        axs[1].set_title('Transitivity of input graph=' + str('%.3f'%(transitivity)))
        axs[1].set_xlabel('Transitivity of random graphs')
        axs[2].hist(case_4_random_measures[2,:], bins='auto')
        axs[2].set_title('Avg. cluster of input graph=' + str('%.3f'%(avg_cluster)))
        axs[2].set_xlabel('Avg. cluster of random graphs')
        fig.tight_layout(pad=3.0)
        plt.show(block=False)

    def test_graph5(self): #high in clusters
        A = np.array([[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,1,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)

        char_path_length = graph.get_measure(MeasurePathLength, 'char_path_length')
        transitivity = graph.get_measure(MeasureTransitivity, 'transitivity')
        avg_cluster = graph.get_measure(MeasureCluster, 'avg_cluster')
        print('')
        print('Case 5, with BD of size: ', A.shape)
        print('Char. path length: ', char_path_length)
        print('Transitivity: ', transitivity)
        print('Avg. cluster: ', avg_cluster)

        random = graph.get_random_graph()
        random = GraphBD(random, graph.settings)
        self.assertTrue(random.A.shape == A.shape)
        self.assertEqual(np.sum(random.A), np.sum(A))

        case_5_random_measures = np.zeros((3, 1000))
        for i in range(0,1000):
            random = graph.get_random_graph()
            random = GraphBD(random, graph.settings)

            char_path_length_random = random.get_measure(MeasurePathLength, 'char_path_length')
            case_5_random_measures[0,i] = char_path_length_random

            transitivity_random = random.get_measure(MeasureTransitivity, 'transitivity')
            case_5_random_measures[1,i] = transitivity_random

            avg_cluster_random = random.get_measure(MeasureCluster, 'avg_cluster')
            case_5_random_measures[2,i] = avg_cluster_random

        fig, axs = plt.subplots(3)
        fig.suptitle('Test case 5: input BD graph dim=' + str(A.shape))
        axs[0].hist(case_5_random_measures[0,:], bins='auto')
        axs[0].set_title('Char. path length of input graph=' + str('%.3f'%(char_path_length)))
        axs[0].set_xlabel('Char. path length of random graphs')
        axs[1].hist(case_5_random_measures[1,:], bins='auto')
        axs[1].set_title('Transitivity of input graph=' + str('%.3f'%(transitivity)))
        axs[1].set_xlabel('Transitivity of random graphs')
        axs[2].hist(case_5_random_measures[2,:], bins='auto')
        axs[2].set_title('Avg. cluster of input graph=' + str('%.3f'%(avg_cluster)))
        axs[2].set_xlabel('Avg. cluster of random graphs')
        fig.tight_layout(pad=3.0)
        plt.show(block=False)

    def test_graph6(self): #as above but with more random connections
        A = np.array([[0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
                      [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
                      [0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0],
                      [0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0],
                      [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                      [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1],
                      [0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                      [0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                      [1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                      [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
                      [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                      [0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
                      [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
                      [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0],
                      [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
                      [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,1,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
                      [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1],
                      [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]])
        settings = GraphSettings.get_bd()
        graph = GraphFactory.get_graph(A, settings)

        char_path_length = graph.get_measure(MeasurePathLength, 'char_path_length')
        transitivity = graph.get_measure(MeasureTransitivity, 'transitivity')
        avg_cluster = graph.get_measure(MeasureCluster, 'avg_cluster')
        print('')
        print('Case 6, with BD of size: ', A.shape)
        print('Char. path length: ', char_path_length)
        print('Transitivity: ', transitivity)
        print('Avg. cluster: ', avg_cluster)

        random = graph.get_random_graph()
        random = GraphBD(random, graph.settings)
        self.assertTrue(random.A.shape == A.shape)
        self.assertEqual(np.sum(random.A), np.sum(A))

        case_6_random_measures = np.zeros((3, 1000))
        for i in range(0,1000):
            random = graph.get_random_graph()
            random = GraphBD(random, graph.settings)

            char_path_length_random = random.get_measure(MeasurePathLength, 'char_path_length')
            case_6_random_measures[0,i] = char_path_length_random

            transitivity_random = random.get_measure(MeasureTransitivity, 'transitivity')
            case_6_random_measures[1,i] = transitivity_random

            avg_cluster_random = random.get_measure(MeasureCluster, 'avg_cluster')
            case_6_random_measures[2,i] = avg_cluster_random

        fig, axs = plt.subplots(3)
        fig.suptitle('Test case 6: input BD graph dim=' + str(A.shape))
        axs[0].hist(case_6_random_measures[0,:], bins='auto')
        axs[0].set_title('Char. path length of input graph=' + str('%.3f'%(char_path_length)))
        axs[0].set_xlabel('Char. path length of random graphs')
        axs[1].hist(case_6_random_measures[1,:], bins='auto')
        axs[1].set_title('Transitivity of input graph=' + str('%.3f'%(transitivity)))
        axs[1].set_xlabel('Transitivity of random graphs')
        axs[2].hist(case_6_random_measures[2,:], bins='auto')
        axs[2].set_title('Avg. cluster of input graph=' + str('%.3f'%(avg_cluster)))
        axs[2].set_xlabel('Avg. cluster of random graphs')
        fig.tight_layout(pad=3.0)
        plt.show()

if __name__ == '__main__':
    unittest.main()