from braphy.graph_measures.measure import Measure
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
        # Need to add functionality for undirected
        
        M = 100
        C = graph.get_measure(MeasureCluster, 'cluster')

        if graph.is_directed():
            L = graph.get_measure(Measure, 'char_path_length')
        else:
            pass

        Cr = np.zeros(M)
        Lr = np.zeros(M)

        for i in range(M):
            gr = g.FUNCTION_FOR_RANDOM_GRAPH ##################################
            Cr[i] = gr.get_measure(MeasureCluster, 'cluster')

            if graph.is_directed():
                Lr(i) = gr.get_measure(MeasurePathLength, 'char_path_length')
            else:
                Lr(i) = gr.get_measure(MeasurePathLength, 'CPl_WSG?????') 
                #################### matlab code for wsg
                #   case Graph.CPL_WSG
                #   tmp = g.pl();
                #   res = mean(tmp(isfinite(tmp)));

        Cr = np.mean(Cr)
        Lr = np.mean(Lr)

        graph.measure_dict[MeasureSmallWorldness]['small_worldness'] = (C/Cr)/(L/Lr) 

        def get_valid_graph_types():
            graph_type_measures = {}
            graph_type_measures[GraphBD] = ['cluster', 'avg_cluster']
            graph_type_measures[GraphBU] = ['cluster', 'avg_cluster']
            graph_type_measures[GraphWD] = ['cluster', 'avg_cluster']
            graph_type_measures[GraphWU] = ['cluster', 'avg_cluster']
            return graph_type_measures