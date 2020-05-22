class Measurement():
    def __init__(self, group, measure_class, sub_measure, value = None):
        self.group = group
        self.measure_class = measure_class
        self.sub_measure = sub_measure
        self.value = value

    def get_value(self):
        return self.value
