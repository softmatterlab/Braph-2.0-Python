from braphy.analysis.random_comparison import RandomComparison

class RandomComparisonFunctional(RandomComparison):
    def __init__(self, group_index, measure_class, sub_measure,
                 attempts_per_edge, number_of_weights,
                 randomization_number, measure, mean_random_measures,
                 difference, differences, p_values,
                 confidence_intervals, binary_value):
        super().__init__(group_index, measure_class, sub_measure,
                         attempts_per_edge, number_of_weights,
                         randomization_number, measure, mean_random_measures,
                         difference, differences, p_values,
                         confidence_intervals, binary_value)
