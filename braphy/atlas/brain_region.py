import numpy as np
import xml.etree.ElementTree as ET

class BrainRegion():
    def __init__(self, label = 'BR', name = 'br_name', x = 0, y = 0, z = 0):
        self.observers = []
        self.label = label
        self.name = name
        self.x = x
        self.y = y
        self.z = z

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
        s = '<BrainRegion label="{}" name="{}" x="{}" y="{}" z="{}"/>'.format(
             self.label,
             self.name,
             self.x,
             self.y,
             self.z)
        return s

    def __str__(self):
        s = "{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(self.label,
                                                  self.name,
                                                  self.x,
                                                  self.y,
                                                  self.z)
        return s

    def __eq__(self, other):
        if not isinstance(other, BrainRegion):
            return NotImplemented

        return (self.label, self.name, self.x, self.y, self.z) == (other.label, \
                other.name, other.x, other.y, other.z)

    def to_dict(self):
        d = {}
        d['label'] = self.label
        d['name'] = self.name
        d['x'] = self.x
        d['y'] = self.y
        d['z'] = self.z
        return d

    def from_dict(d):
        return BrainRegion(label = d['label'],
                           name = d['name'],
                           x = d['x'],
                           y = d['y'],
                           z = d['z'])
