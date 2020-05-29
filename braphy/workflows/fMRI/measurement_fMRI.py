from braphy.analysis.measurement import Measurement

class MeasurementfMRI(Measurement):
    def __init__(self, group, measure_class, sub_measure, values = None):
        super().__init__(group, measure_class, sub_measure, values)