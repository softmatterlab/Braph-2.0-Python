from braphy.analysis.measurement import Measurement

class MeasurementMRI(Measurement):
    def __init__(self, group, measure_class, sub_measure, value = None):
        super().__init__(group, measure_class, sub_measure, value)