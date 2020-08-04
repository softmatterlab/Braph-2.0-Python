from braphy.graph.graphs.graph import Graph
from braphy.graph.measures import *
from braphy.graph.measures.measure_parser import MeasureParser

class GraphSettings():
    WEIGHTED_DEFAULT = True
    DIRECTED_DEFAULT = True
    GAMMA_DEFAULT = 1
    COMMUNITY_ALGORITHM_DEFAULT = 'Louvain'
    NEGATIVE = ['zero', 'none', 'abs']
    STANDARDIZE = ['range', 'threshold']
    SYMMETRIZE = ['max', 'min', 'sum', 'average']
    BINARY = ['threshold', 'density']
    BINARY_VALUE_DEFAULT = 0
    CORRELATION_TYPE = ['pearson', 'spearman', 'kendall', 'partial pearson', 'partial spearman']

    def __init__(self, weighted = WEIGHTED_DEFAULT, directed = DIRECTED_DEFAULT,
                 gamma = GAMMA_DEFAULT, community_algorithm = COMMUNITY_ALGORITHM_DEFAULT,
                 rule_negative = NEGATIVE[0], rule_symmetrize = SYMMETRIZE[0],
                 rule_standardize = STANDARDIZE[0], rule_binary = BINARY[0],
                 value_binary = BINARY_VALUE_DEFAULT, correlation_type = CORRELATION_TYPE[0]):
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
        gamma = d['gamma']
        community_algorithm = d['community_algorithm']
        rule_negative = d['rule_negative']
        rule_symmetrize = d['rule_symmetrize']
        rule_standardize = d['rule_standardize']
        rule_binary = d['rule_negative']
        value_binary = d['value_binary']
        correlation_type = d['correlation_type']
        return GraphSettings(weighted, directed, gamma, community_algorithm,
                             rule_negative, rule_symmetrize, rule_standardize, rule_binary,
                             value_binary, correlation_type)

    def graph_class(self):
        cls = None
        for graph in Graph.__subclasses__():
            match = True
            for key, value in graph.match_settings().items():
                if(eval('self.{}'.format(key)) != value):
                    match = False
            if match:
                cls = graph
                break
        return cls

class GraphFactory:
    def get_graph(A, settings):
        return settings.graph_class()(A, settings)
