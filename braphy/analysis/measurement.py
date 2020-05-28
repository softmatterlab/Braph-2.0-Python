class Measurement():
    def __init__(self, group, measure_class, sub_measure, value = None):
        self.group = group
        self.measure_class = measure_class
        self.sub_measure = sub_measure
        self.value = value

    def get_value(self):
        return self.value

    def is_global(self):
        return self.measure_class.is_global(self.sub_measure)

    def is_nodal(self):
        return self.measure_class.is_nodal(self.sub_measure)

    def is_binodal(self):
        return self.measure_class.is_binodal(self.sub_measure)

    def dimension(self):
        return self.measure_class.dimension(self.sub_measure)
