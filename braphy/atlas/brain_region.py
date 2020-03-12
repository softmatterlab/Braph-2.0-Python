import numpy as np
import xml.etree.ElementTree as ET

class BrainRegion():
    def __init__(self, label = 'BR', name = 'br_name', x = 0, y = 0, z = 0, hemisphere = ".", notes = "."):
        self.observers = []
        self.label = label
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.hemisphere = hemisphere
        self.notes = notes

    def set(self, **kwargs):
        self.__dict__.update(kwargs)
        self.notify_observers()

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer()

    def to_string(self):
        pass

    def disp(self):
        pass

    def get_position(self):
        position = np.array([self.x, self.y, self.z])
        return position

    def set_xml(self, parent):
        ET.SubElement(parent, self.str_xml())

    def str_xml(self):
        s = 'BrainRegion hemisphere="{}" label="{}" name="{}" notes="{}" x="{}" y="{}" z="{}"'.format(
             self.hemisphere,
             self.label,
             self.name,
             self.notes,
             self.x,
             self.y,
             self.z)
        return s

    def __str__(self):
        s = "{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(self.label,
                                                  self.name,
                                                  self.x,
                                                  self.y,
                                                  self.z,
                                                  self.hemisphere,
                                                  self.notes)
        return s

    def __eq__(self, other):
        if not isinstance(other, BrainRegion):
            return NotImplemented

        return (self.label, self.name, self.x, self.y, self.z) == (other.label, \
                other.name, other.x, other.y, other.z)
