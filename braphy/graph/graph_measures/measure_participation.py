from braphy.graph.graph_measures.measure import Measure
from braphy.graph.graph_measures.measure_degree import MeasureDegree
from braphy.graph.graph_measures.measure_community_structure import MeasureCommunityStructure
from braphy.utility.helper_functions import divide_without_warning
import numpy as np
from braphy.graph.graphs import *
import copy

class MeasureParticipation(Measure):

    def get_description():
        description = {}
        description['participation'] = 'The complementary participation coefficient assesses ' +\
                                        'the diversity of intermodular interconnections of individual nodes. ' +\
                                        'Nodes with a high within-module degree but with a low participation ' +\
                                        'coefficient (known as provincial hubs) are hence likely to play an ' +\
                                        'important part in the facilitation of modular segregation. ' +\
                                        'On the other hand, nodes with a high participation coefficient (known ' +\
                                        'as connector hubs) are likely to facilitate global intermodular integration.'
        return description
    def compute_measure(graph):
        edges = np.sum(graph.A, 1)
        n = np.size(graph.A, 0)

        community_structure = graph.get_measure(MeasureCommunityStructure, 'community_structure')
        community_affiliation = (graph.A != 0).dot(np.diag(community_structure + 1))
        community_neighbours = np.zeros(n)
        for i in range(1, np.max(community_structure)+2):
            community_neighbours = community_neighbours + (np.sum(graph.A*(community_affiliation==i), 1)**2)

        participation = np.ones(n) - divide_without_warning(community_neighbours, (edges**2))
        participation[edges == 0] = 0
        graph.measure_dict[MeasureParticipation]['participation'] = participation

    def get_valid_graph_types():
        graph_type_measures = {}
        graph_type_measures[GraphBD] = ['participation']
        graph_type_measures[GraphBU] = ['participation']
        graph_type_measures[GraphWD] = ['participation']
        graph_type_measures[GraphWU] = ['participation']

        return graph_type_measures

    def community_dependent():
        return True
