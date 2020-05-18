from braphy.analysis.analysis import Analysis

class AnalysisMRI(Analysis):
    def __init__(self, cohort, name = 'analysis', measurements = None, random_comparisons = None, comparisons = None):
        super().__init__(cohort, name, measurements, random_comparisons, comparisons)

    def calculate_measurement(self, measure_class, measure, group_index):
        graph = self.get_graph(group_index)
        measure = graph.get_measure(measure_class, measure, save = False)

        measurement = Measurement('id', 'atlas', group_index, measure)
        return measurement

    def get_graph(self, group_index):
        A = self.get_correlation(group_index)
        return GraphFactory.get_graph(A, self.graph_settings)
