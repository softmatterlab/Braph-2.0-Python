from braphy.analysis.comparison import Comparison

class ComparisonfMRI(Comparison):
    def __init__(self, groups, measure_class, sub_measure, all_differences, p_values,
                 confidence_interval, measures, permutations):
        super().__init__(groups, permutations)
        self.measure_class = measure_class
        self.sub_measure = sub_measure
        self.all_differences = all_differences
        self.p_values = p_values
        self.confidence_interval = confidence_interval
        self.measures = measures