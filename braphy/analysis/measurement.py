from braphy.graph.measures import *

class Measurement():
    def __init__(self, group, measure_class, sub_measure, value = None, binary_value = 0):
        self.group = group
        self.measure_class = measure_class
        self.sub_measure = sub_measure
        self.value = value
        self.binary_value = binary_value

    def to_dict(self):
        d = {}
        d['group'] = str(self.group)
        d['measure_class'] = self.measure_class.__name__
        d['sub_measure'] = self.sub_measure
        d['value'] = self.value.tolist() if isinstance(self.value, np.ndarray) else self.value
        d['binary_value'] = self.binary_value
        return d

    @classmethod
    def from_dict(cls, d):
        group = int(d['group'])
        measure_class = eval(d['measure_class'])
        sub_measure = d['sub_measure']
        value = d['value']
        value = np.array(value) if isinstance(value, list) else value
        binary_value = d['binary_value']
        return cls(group, measure_class, sub_measure, value, binary_value)

    def equal(self, other):
        if not isinstance(other, Measurement):
            return False
        eq = (self.measure_class == other.measure_class and
              self.sub_measure == other.sub_measure and
              self.group == other.group and
              self.binary_value == other.binary_value)
        return eq

    def get_value(self):
        return self.value

    def is_global(self):
        return self.measure_class.is_global(self.sub_measure)

    def is_nodal(self):
        return self.measure_class.is_nodal(self.sub_measure)

    def is_binodal(self):
        return self.measure_class.is_binodal(self.sub_measure)

    def dimension(self):
        return self.measure_class.dimension(self.sub_measure)
