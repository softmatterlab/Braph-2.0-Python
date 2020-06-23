from braphy.analysis.measurement import Measurement

class MeasurementfMRI(Measurement):
    def __init__(self, group, measure_class, sub_measure, value = None, binary_value = 0):
        super().__init__(group, measure_class, sub_measure, values, binary_value)
