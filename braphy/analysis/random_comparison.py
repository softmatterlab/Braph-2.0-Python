class RandomComparison():
    def __init__(self, id, atlas, group):
        self.id = id
        self.atlas = atlas
        self.group = group

    def dimension(self):
        return self.measure_class.dimension(self.sub_measure)