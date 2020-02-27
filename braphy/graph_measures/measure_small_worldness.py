from braphy.graph_measures import *# .measure import Measure
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
            L = graph.get_measure(MeasurePathLength, 'char_path_length')
        else:
            tmp = graph.get_measure(MeasurePathLength, 'path_length')
            res = np.mean(tmp[np.isfinite(tmp)])
            L = res

        Cr = np.empty((M, graph.A.shape[1]))
        print(Cr.shape)
        Lr = np.empty((M, graph.A.shape[1]))

        for i in range(M):
            gr = graph.get_random_graph()
            print(gr.get_measure(MeasureCluster, 'cluster'))
            Cr[i] = gr.get_measure(MeasureCluster, 'cluster')

            if graph.is_directed():
                Lr[i] = gr.get_measure(MeasurePathLength, 'char_path_length')
            else:
                #Lr[i] = gr.get_measure(MeasurePathLength, 'CPl_WSG?????')
                tmp = gr.get_measure(MeasurePathLength, 'path_length')
                res = np.mean(tmp[np.isfinite(tmp)])
                Lr[i] = res
                #print(res)
                #################### matlab code for wsg
                #   case Graph.CPL_WSG
                #   tmp = g.pl();
                #   res = mean(tmp(isfinite(tmp)));

        Cr = np.mean(Cr)
        Lr = np.mean(Lr)

        graph.measure_dict[MeasureSmallWorldness]['small_worldness'] = (C/Cr)/(L/Lr)
        print((C/Cr)/(L/Lr))

    def get_valid_graph_types():
        graph_type_measures = {}
        txt = ['small_worldness']
        graph_type_measures[GraphBD] = txt
        graph_type_measures[GraphBU] = txt
        graph_type_measures[GraphWD] = txt
        graph_type_measures[GraphWU] = txt
        return graph_type_measures