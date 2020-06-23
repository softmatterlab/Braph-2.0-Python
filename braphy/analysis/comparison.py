from braphy.graph.measures import *
import numpy as np

class Comparison():
    def __init__(self, groups, measure_class, sub_measure, all_differences = None, p_values = None,
                 confidence_interval = None, measures = None, permutations = 0, binary_value = 0):
        self.groups = groups
        self.measure_class = measure_class
        self.sub_measure = sub_measure
        self.all_differences = all_differences
        self.p_values = p_values
        self.confidence_interval = confidence_interval
        self.measures = measures
        self.permutations = permutations
        self.binary_value = binary_value

    def equal(self, other):
        if type(self) != type(other):
            return False
        eq = (self.groups[0] == other.groups[0] and
              self.groups[1] == other.groups[1] and
              self.measure_class == other.measure_class and
              self.sub_measure == other.sub_measure and
              self.permutations == other.permutations and
              self.binary_value == other.binary_value)
        return eq

    def to_dict(self):
        d = {}
        d['groups'] = [str(group) for group in self.groups]
        d['measure_class'] = self.measure_class.__name__
        d['sub_measure'] = self.sub_measure
        d['all_differences'] = self.all_differences.tolist()
        if isinstance(self.p_values[0], np.ndarray):
            p_values = [self.p_values[0].tolist(), self.p_values[1].tolist()]
        else:
            p_values = [self.p_values[0], self.p_values[1]]
        d['p_values'] = p_values
        if isinstance(self.measures[0], np.ndarray):
            measures = [self.measures[0].tolist(), self.measures[1].tolist()]
        else:
            measures = [self.measures[0], self.measures[1]]
        d['measures'] = measures
        d['confidence_interval'] = ''
        d['permutations'] = self.permutations
        return d

    @classmethod
    def from_dict(cls, d):
        groups = [int(group) for group in d['groups']]
        measure_class = eval(d['measure_class'])
        sub_measure = d['sub_measure']
        all_differences = np.array(d['all_differences'])
        p_values = d['p_values']
        if isinstance(p_values[0], list):
            p_values = (np.array(p_values[0]), np.array(p_values[1]))
        else:
            p_values = (p_values[0], p_values[1])
        confidence_interval = (0, 0)
        measures = d['measures']
        if isinstance(measures[0], list):
            measures = (np.array(measures[0]), np.array(measures[1]))
        else:
            measures = (measures[0], measures[1])
        permutations = d['permutations']

        return cls(groups, measure_class, sub_measure, all_differences, p_values, confidence_interval, measures, permutations)

    def dimension(self):
        return self.measure_class.dimension(self.sub_measure)
