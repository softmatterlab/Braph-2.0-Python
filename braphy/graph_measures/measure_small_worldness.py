from braphy.graph_measures import *
import numpy as np
from braphy.graph import *
import copy

class MeasureSmallWorldness(Measure):

    def get_description():
        # Exists one more measure
        description = {}

        description['small_worldness'] = 'Network small-worldness.'
        
        return description

    def compute_measure(graph):
                
        M = 100
        C = graph.get_measure(MeasureCluster, 'cluster')

        if graph.is_directed():
            L = graph.get_measure(MeasurePathLength, 'char_path_length')
        else:
            L = graph.get_measure(MeasurePathLength, 'char_path_length_wsg')


        Cr = np.empty((M, graph.A.shape[1]))
        Lr = np.empty((M, graph.A.shape[1]))

        for i in range(M):
            gr = graph.get_random_graph()
            Cr[i] = gr.get_measure(MeasureCluster, 'cluster')

            if graph.is_directed():
                Lr[i] = gr.get_measure(MeasurePathLength, 'char_path_length')
            else:
                Lr[i] = gr.get_measure(MeasurePathLength, 'char_path_length_wsg')

        Cr = np.mean(Cr)
        Lr = np.mean(Lr)

        graph.measure_dict[MeasureSmallWorldness]['small_worldness'] = (C/Cr)/(L/Lr)

    def get_valid_graph_types():
        graph_type_measures = {}
        txt = ['small_worldness']
        graph_type_measures[GraphBD] = txt
        graph_type_measures[GraphBU] = txt
        graph_type_measures[GraphWD] = txt
        graph_type_measures[GraphWU] = txt
        return graph_type_measures