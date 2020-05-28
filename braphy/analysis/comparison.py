class Comparison():
    def __init__(self, groups, permutations):
        self.groups = groups
        self.permutations = permutations

    def dimension(self):
        return self.measure_class.dimension(self.sub_measure)