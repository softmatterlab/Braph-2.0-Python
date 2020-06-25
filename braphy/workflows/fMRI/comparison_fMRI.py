from braphy.analysis.comparison import Comparison

class ComparisonfMRI(Comparison):
    def __init__(self, groups, measure_class, sub_measure, all_differences = None, p_values = None,
            confidence_interval = None, measures = None, permutations = 0, binary_value = 0, longitudinal = False):
        super().__init__(groups, measure_class, sub_measure, all_differences, p_values,
                 confidence_interval, measures, permutations, binary_value, longitudinal)
