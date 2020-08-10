class RandomComparison():
    def __init__(self, group_index, measure_class, sub_measure,
                 attempts_per_edge, number_of_weights,
                 randomization_number, measure, mean_random_measures,
                 difference, differences, p_values,
                 confidence_intervals, binary_value):
        self.group_index = group_index
        self.measure_class = measure_class
        self.sub_measure = sub_measure
        self.attempts_per_edge = attempts_per_edge
        self.number_of_weights = number_of_weights
        self.randomization_number = randomization_number
        self.measure = measure
        self.mean_random_measures = mean_random_measures
        self.difference = difference
        self.differences = differences
        self.p_values = p_values
        self.confidence_intervals = confidence_intervals
        self.binary_value = binary_value

    def equals(self, other):
        if not isinstance(other, RandomComparison):
            return False
        eq = (self.group_index == other.group_index and
              self.measure_class == other.measure_class and
              self.sub_measure == other.sub_measure and
              self.attempts_per_edge == other.attempts_per_edge and
              self.number_of_weights == other.number_of_weights and
              self.randomization_number == other.randomization_number and
              self.binary_value == other.binary_value)
        return eq

    def to_dict(self):
        d = {}
        d['group_index'] = self.group_index
        d['measure_class'] = self.measure_class.__name__
        d['sub_measure'] = self.sub_measure
        d['attempts_per_edge'] = self.attempts_per_edge
        d['number_of_weights'] = self.number_of_weights
        d['randomization_number'] = self.randomization_number
        d['measure'] = self.measure
        d['mean_random_measures'] = self.mean_random_measures
        d['difference'] = self.difference
        d['differences'] = self.differences.tolist()

        if isinstance(self.p_values[0], np.ndarray):
            p_values = [self.p_values[0].tolist(), self.p_values[1].tolist()]
        else:
            p_values = [self.p_values[0], self.p_values[1]]
        d['p_values'] = p_values

        if isinstance(self.confidence_intervals[0], np.ndarray):
            confidence_intervals = [self.confidence_intervals[0].tolist(), self.confidence_intervals[1].tolist()]
        else:
            confidence_intervals = [self.confidence_intervals[0], self.confidence_intervals[1]]
        d['confidence_intervals'] = confidence_intervals
        d['binary_value'] = self.binary_value
        return d

    @classmethod
    def from_dict(cls, d):
        group_index = int(d['group_index'])
        measure_class = eval(d['measure_class'])
        sub_measure = d['sub_measure']
        attempts_per_edge = d['attempts_per_edge']
        number_of_weights = d['number_of_weights']
        randomization_number = d['randomization_number']
        measure = d['measure']
        mean_random_measures = d['mean_random_measures']
        difference = d['difference']
        differences = np.array(d['differences'])
        p_values = d['p_values']
        if isinstance(p_values[0], list):
            p_values = (np.array(p_values[0]), np.array(p_values[1]))
        else:
            p_values = (p_values[0], p_values[1])
        confidence_intervals = d['p_values']
        if isinstance(confidence_intervals[0], list):
            confidence_intervals = (np.array(p_values[0]), np.array(p_values[1]))
        else:
            confidence_intervals = (p_values[0], p_values[1])
        binary_value = d['binary_value']

        return cls(group_index, measure_class, sub_measure, attempts_per_edge, number_of_weights,
                   randomization_number, measure, mean_random_measures, difference, differences,
                   p_values, confidence_intervals, binary_value)

    def dimension(self):
        return self.measure_class.dimension(self.sub_measure)
