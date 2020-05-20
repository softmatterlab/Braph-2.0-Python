from braphy.analysis.comparison import Comparison

class ComparisonMRI(Comparison):
    def __init__(self, id, atlas, groups):
        super().__init__(id, atlas, groups)