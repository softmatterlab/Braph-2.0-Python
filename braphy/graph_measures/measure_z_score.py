from braphy.graph_measures.measure import Measure
import numpy as np
from braphy.graph import *
from braphy.utility.helper_functions import divide_without_warning
import copy

class MeasureZScore(Measure):

    def get_description():
        description = {}
        description['z_score'] = 'The within-module degree z-score of a node is a within-module version ' +\
                                 'of degree centrality. This measure requires a previously determined community structure.'
        description['in_z_score'] = 'The within-module degree in-z-score of a node is a within-module ' +\
                                    'version of degree centrality. This measure requires a previously ' +\
                                    'determined community structure.'
        description['out_z_score'] = 'The within-module degree out-z-score of a node is a within-module ' +\
                                     'version of degree centrality. This measure requires a previously ' +\
                                     'determined community structure.'
        return description

    def compute_measure(graph):
        z_score = MeasureZScore.z_score(graph.A + graph.A.T, graph.community_structure)
        graph.measure_dict[MeasureZScore]['z_score'] = z_score
        if graph.is_directed():
            in_z_score = MeasureZScore.z_score(graph.A, graph.community_structure)
            out_z_score = MeasureZScore.z_score(graph.A.T, graph.community_structure)
            graph.measure_dict[MeasureZScore]['in_z_score'] = in_z_score
            graph.measure_dict[MeasureZScore]['out_z_score'] = out_z_score

    def z_score(W, community):
        n = np.size(W, 0)
        z_score = np.zeros(n)
        for i in range(np.max(community)+1):
            idx = np.where(community == i)[0]
            koi = np.sum(W[idx, :][:, idx], 1)
            z_score[idx] = divide_without_warning(koi-np.mean(koi), np.std(koi, ddof=1))
        z_score[np.isnan(z_score)] = 0
        return z_score

    def get_valid_graph_types():
        graph_type_measures = {}

        graph_type_measures[GraphBD] = ['z_score', 'out_z_score', 'in_z_score']
        graph_type_measures[GraphBU] = ['z_score']
        graph_type_measures[GraphWD] = ['z_score', 'out_z_score', 'in_z_score']
        graph_type_measures[GraphWU] = ['z_score']

        return graph_type_measures

    def community_dependent():
        return True
