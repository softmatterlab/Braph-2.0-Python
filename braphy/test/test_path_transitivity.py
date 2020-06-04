import unittest
from braphy.graph.graph_factory import GraphFactory, GraphSettings
from braphy.graph.measures.measure_path_transitivity import MeasurePathTransitivity
from braphy.test.test_utility import TestUtility
import numpy as np

class TestPathTransitivity(TestUtility):
    def test_graphBU1(self):
        A = np.array([[0,1,1,1], [1,0,1,0], [1,1,0,0], [1,0,0,0]])
        settings = GraphSettings.get_bu()
        graph = GraphFactory.get_graph(A, settings)
        path_transitivity = np.array([[0.,0.666667,0.666667,0.],[0.666667,0.,1.,0.44444],
                                        [0.666667,1.,0.,0.44444],[0.,0.44444,0.44444,0.]])
        self.assertMatrixAlmostEqual(graph.get_measure(MeasurePathTransitivity, 'path_transitivity'),
                                    path_transitivity, 4)

    def test_graphBU2(self):
        A = np.array([[0,1,0,1,0,1], [1,0,1,0,1,1], [0,1,0,1,1,1], [1,0,1,0,0,1], 
                    [0,1,1,0,0,1], [1,1,1,1,1,0]])
        settings = GraphSettings.get_bu()
        graph = GraphFactory.get_graph(A, settings)
        path_transitivity = np.array([[0,0.4000,0.5714,0.5000,0.4444,0.6667],
                                      [0.4000,0,0.6667,0.5714,0.8000,0.8571],
                                      [0.5714,0.6667,0,0.4000,0.8000,0.8571],
                                      [0.5000,0.5714,0.4000,0,0.4444,0.6667],
                                      [0.4444,0.8000,0.8000,0.4444,0,0.6667],
                                      [0.6667,0.8571,0.8571,0.6667,0.6667,0]])
        self.assertMatrixAlmostEqual(graph.get_measure(MeasurePathTransitivity, 'path_transitivity'),
                                    path_transitivity, 4)

if __name__ == '__main__':
    unittest.main()