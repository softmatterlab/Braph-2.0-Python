class RandomComparison():
    def __init__(self, id, atlas, group):
        self.id = id
        self.atlas = atlas
        self.group = group

    def to_dict(self):
        d = {}
        d['id'] = self.id
        return d

    def from_dict(self):
        return RandomComparison(d['id'], None, None)

    def dimension(self):
        return self.measure_class.dimension(self.sub_measure)
