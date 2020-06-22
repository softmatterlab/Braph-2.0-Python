from braphy.analysis.comparison import Comparison

class ComparisonMRI(Comparison):
    def __init__(self, groups, measure_class, sub_measure, all_differences, p_values,
                 confidence_interval, measures, permutations):
        super().__init__(groups, measure_class, sub_measure, all_differences, p_values,
                 confidence_interval, measures, permutations)
