from braphy.analysis.random_comparison import RandomComparison

class RandomComparisonMRI(RandomComparison):
    def __init__(self, id, atlas, group):
        super().__init__(id, atlas, group)