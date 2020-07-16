from braphy.graph.graphs import *
from braphy.graph.measures import *
from braphy.graph.measures.measure_parser import MeasureParser

class GraphSettings():
    GAMMA_DEFAULT = 1
    COMMUNITY_ALGORITHM_DEFAULT = 'Louvain'
    NEGATIVE_DEFAULT = 'zero'
    STANDARDIZE_DEFAULT = 'range'
    SYMMETRIZE_DEFAULT = 'max'
    BINARY_DEFAULT = 'threshold'
    BINARY_VALUE_DEFAULT = 0
    CORRELATION_TYPE_DEFAULT = 'pearson'

    def __init__(self, weighted, directed, gamma, community_algorithm, rule_negative,
                 rule_symmetrize, rule_standardize, rule_binary, value_binary, correlation_type):
        self.weighted = weighted
        self.directed = directed
        self.measure_list = MeasureParser.list_measures()[self.graph_class()]
        self.gamma = gamma
        self.community_algorithm = community_algorithm
        self.rule_negative = rule_negative
        self.rule_symmetrize = rule_symmetrize
        self.rule_standardize = rule_standardize
        self.rule_binary = rule_binary
        self.value_binary = value_binary
        self.correlation_type = correlation_type

    def to_dict(self):
        d = {}
        d['weighted'] = self.weighted
        d['directed'] = self.directed
        measure_dict = {}
        for measure_class, sub_measure_list in self.measure_list.items():
            measure_dict[measure_class.__name__] = sub_measure_list
        d['measure_list'] = measure_dict
        d['gamma'] = self.gamma
        d['community_algorithm'] = self.community_algorithm
        d['rule_negative'] = self.rule_negative
        d['rule_symmetrize'] = self.rule_symmetrize
        d['rule_standardize'] = self.rule_standardize
        d['rule_binary'] = self.rule_binary
        d['value_binary'] = self.value_binary
        d['correlation_type'] = self.correlation_type
        return d

    def from_dict(d):
        weighted = d['weighted']
        directed = d['directed']
        measure_list = {}
        for measure_class_str, sub_measure_list in d['measure_list'].items():
            measure_list[eval(measure_class_str)] = sub_measure_list
        gamma = d['gamma']
        community_algorithm = d['community_algorithm']
        rule_negative = d['rule_negative']
        rule_symmetrize = d['rule_symmetrize']
        rule_standardize = d['rule_standardize']
        rule_binary = d['rule_negative']
        value_binary = d['value_binary']
        correlation_type = d['correlation_type']
        return GraphSettings(weighted, directed, measure_list, gamma, community_algorithm,
                             rule_negative, rule_symmetrize, rule_standardize, rule_binary,
                             value_binary, correlation_type)

    def get_bd(gamma = GAMMA_DEFAULT,
               community_algorithm = COMMUNITY_ALGORITHM_DEFAULT,
               rule_negative = NEGATIVE_DEFAULT, rule_symmetrize = SYMMETRIZE_DEFAULT,
               rule_standardize = STANDARDIZE_DEFAULT, rule_binary = BINARY_DEFAULT,
               value_binary = BINARY_VALUE_DEFAULT, correlation_type = CORRELATION_TYPE_DEFAULT):
        return GraphSettings(weighted = False,
                             directed = True,
                             gamma = gamma,
                             community_algorithm = community_algorithm,
                             rule_negative = rule_negative,
                             rule_symmetrize = rule_symmetrize,
                             rule_standardize = rule_standardize,
                             rule_binary = rule_binary,
                             value_binary = value_binary,
                             correlation_type = correlation_type)

    def get_bu(gamma = GAMMA_DEFAULT,
               community_algorithm = COMMUNITY_ALGORITHM_DEFAULT,
               rule_negative = NEGATIVE_DEFAULT, rule_symmetrize = SYMMETRIZE_DEFAULT,
               rule_standardize = STANDARDIZE_DEFAULT, rule_binary = BINARY_DEFAULT,
               value_binary = BINARY_VALUE_DEFAULT, correlation_type = CORRELATION_TYPE_DEFAULT):
        return GraphSettings(weighted = False,
                             directed = False,
                             gamma = gamma,
                             community_algorithm = community_algorithm,
                             rule_negative = rule_negative,
                             rule_symmetrize = rule_symmetrize,
                             rule_standardize = rule_standardize,
                             rule_binary = rule_binary,
                             value_binary = value_binary,
                             correlation_type = correlation_type)

    def get_wd(gamma = GAMMA_DEFAULT,
               community_algorithm = COMMUNITY_ALGORITHM_DEFAULT,
               rule_negative = NEGATIVE_DEFAULT, rule_symmetrize = SYMMETRIZE_DEFAULT,
               rule_standardize = STANDARDIZE_DEFAULT, rule_binary = BINARY_DEFAULT,
               value_binary = BINARY_VALUE_DEFAULT, correlation_type = CORRELATION_TYPE_DEFAULT):
        return GraphSettings(weighted = True,
                             directed = True,
                             gamma = gamma,
                             community_algorithm = community_algorithm,
                             rule_negative = rule_negative,
                             rule_symmetrize = rule_symmetrize,
                             rule_standardize = rule_standardize,
                             rule_binary = rule_binary,
                             value_binary = value_binary,
                             correlation_type = correlation_type)

    def get_wu(gamma = GAMMA_DEFAULT,
               community_algorithm = COMMUNITY_ALGORITHM_DEFAULT,
               rule_negative = NEGATIVE_DEFAULT, rule_symmetrize = SYMMETRIZE_DEFAULT,
               rule_standardize = STANDARDIZE_DEFAULT, rule_binary = BINARY_DEFAULT,
               value_binary = BINARY_VALUE_DEFAULT, correlation_type = CORRELATION_TYPE_DEFAULT):
        return GraphSettings(weighted = True,
                             directed = False,
                             gamma = gamma,
                             community_algorithm = community_algorithm,
                             rule_negative = rule_negative,
                             rule_symmetrize = rule_symmetrize,
                             rule_standardize = rule_standardize,
                             rule_binary = rule_binary,
                             value_binary = value_binary,
                             correlation_type = correlation_type)

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

    def graph_cls_from_str(s):
        graph_type = None
        if s == 'binary undirected':
            graph_type = GraphBU
        elif s == 'binary directed':
            graph_type = GraphBD
        elif s == 'weighted undirected':
            graph_type = GraphWU
        elif s == 'weighted directed':
            graph_type = GraphWD
        return graph_type
