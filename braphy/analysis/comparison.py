class Comparison():
    def __init__(self, groups, permutations):
        self.groups = groups
        self.permutations = permutations

    def to_dict(self):
        d = {}
        d['groups'] = [str(group) for group in self.groups]
        d['permutations'] = self.permutations
        return d

    def from_dict(d):
        groups = [int(group) for group in d['groups']]
        permutations = d['permutations']
        return Comparison(groups, permutations)

    def dimension(self):
        return self.measure_class.dimension(self.sub_measure)
