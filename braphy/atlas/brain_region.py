import numpy as np

class BrainRegion():
    def __init__(self, label = 'BR', name = 'br_name', x = 0, y = 0, z = 0):
        self.label = label
        self.name = name
        self.x = x
        self.y = y
        self.z = z

    def to_string(self):
        pass

    def disp(self):
        pass

    def get_position(self):
        position = np.array([self.x, self.y, self.z])
        return position

    def __eq__(self, other):
        if not isinstance(other, BrainRegion):
            return NotImplemented

        return (self.label, self.name, self.x, self.y, self.z) == (other.label, \
                other.name, other.x, other.y, other.z)