from braphy.graph.graphs import *
from braphy.graph.measures.measure_parser import MeasureParser

class GraphSettings():
    GAMMA_DEFAULT = 1
    COMMUNITY_ALGORITHM_DEFAULT = 'Louvain'
    SEMIPOSITIVIZE_DEFAULT = 'zero'
    STANDARDIZE_DEFAULT = 'range'
    SYMMETRIZE_DEFUALT = 'max'

    def __init__(self, weighted, directed, measure_list, gamma, community_algorithm,
                 rule_semipositivize, rule_symmetrize, rule_standardize):
        self.weighted = weighted
        self.directed = directed
        self.measure_list = measure_list
        self.gamma = gamma
        self.community_algorithm = community_algorithm
        self.rule_semipositivize = rule_semipositivize
        self.rule_symmetrize = rule_symmetrize
        self.rule_standardize = rule_standardize

    def get_bd(measure_list = MeasureParser.list_measures(), gamma = GAMMA_DEFAULT,
               community_algorithm = COMMUNITY_ALGORITHM_DEFAULT,
               rule_semipositivize = SEMIPOSITIVIZE_DEFAULT, rule_symmetrize = SYMMETRIZE_DEFUALT, 
               rule_standardize = STANDARDIZE_DEFAULT):
        return GraphSettings(weighted = False,
                             directed = True,
                             measure_list = measure_list[GraphBD],
                             gamma = gamma,
                             community_algorithm = community_algorithm,
                             rule_semipositivize = rule_semipositivize,
                             rule_symmetrize = rule_symmetrize,
                             rule_standardize = rule_standardize)

    def get_bu(measure_list = MeasureParser.list_measures(), gamma = GAMMA_DEFAULT,
               community_algorithm = COMMUNITY_ALGORITHM_DEFAULT,
               rule_semipositivize = SEMIPOSITIVIZE_DEFAULT, rule_symmetrize = SYMMETRIZE_DEFUALT, 
               rule_standardize = STANDARDIZE_DEFAULT):
        return GraphSettings(weighted = False,
                             directed = False,
                             measure_list = measure_list[GraphBU],
                             gamma = gamma,
                             community_algorithm = community_algorithm,
                             rule_semipositivize = rule_semipositivize,
                             rule_symmetrize = rule_symmetrize,
                             rule_standardize = rule_standardize)

    def get_wd(measure_list = MeasureParser.list_measures(), gamma = GAMMA_DEFAULT,
               community_algorithm = COMMUNITY_ALGORITHM_DEFAULT,
               rule_semipositivize = SEMIPOSITIVIZE_DEFAULT, rule_symmetrize = SYMMETRIZE_DEFUALT, 
               rule_standardize = STANDARDIZE_DEFAULT):
        return GraphSettings(weighted = True,
                             directed = True,
                             measure_list = measure_list[GraphWD],
                             gamma = gamma,
                             community_algorithm = community_algorithm,
                             rule_semipositivize = rule_semipositivize,
                             rule_symmetrize = rule_symmetrize,
                             rule_standardize = rule_standardize)

    def get_wu(measure_list = MeasureParser.list_measures(), gamma = GAMMA_DEFAULT,
               community_algorithm = COMMUNITY_ALGORITHM_DEFAULT,
               rule_semipositivize = SEMIPOSITIVIZE_DEFAULT, rule_symmetrize = SYMMETRIZE_DEFUALT, 
               rule_standardize = STANDARDIZE_DEFAULT):
        return GraphSettings(weighted = True,
                             directed = False,
                             measure_list = measure_list[GraphWU],
                             gamma = gamma,
                             community_algorithm = community_algorithm,
                             rule_semipositivize = rule_semipositivize,
                             rule_symmetrize = rule_symmetrize,
                             rule_standardize = rule_standardize)

    def graph_class(self):
        cls = None
        if(self.weighted and self.directed):
            cls = GraphWD
        elif(not self.weighted and self.directed):
            cls = GraphBD
        elif(not self.weighted and not self.directed):
            cls = GraphBU
        elif(self.weighted and not self.directed):
            cls = GraphWU

        return cls

class GraphFactory:

    def get_graph(A, settings):
        return settings.graph_class()(A, settings)
