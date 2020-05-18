from braphy.analysis.measurement import Measurement

class MeasurementMRI(Measurement):
    def __init__(self, id, atlas, group, measure):
        super().__init__(id, atlas, group, measure)