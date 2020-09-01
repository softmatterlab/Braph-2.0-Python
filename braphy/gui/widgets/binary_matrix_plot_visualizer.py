from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from braphy.utility.math_utility import float_to_string
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

class BinaryMatrixPlotVisualizer(FigureCanvas):
    def __init__(self, parent = None, width = 8, height = 6, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.binary_values = None
        self.toolbar = NavigationToolbar2QT(self, self)
        self.toolbar.hide()
        self.labels_visible = False
        self.colorbar_visible = False
        self.colorbar = None

    def init(self, node_labels, y_label):
        self.node_labels = node_labels
        self.y_label = y_label

    def plot(self, matrix, title = None, binary_values = None):
        self.remove_colorbar()
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.cax = self.ax.imshow(matrix)

        self.set_colorbar()
        self.set_labels(title, binary_values)

        self.figure.tight_layout()
        self.draw()
        self.show_labels()
        self.show_colorbar()

    def get_title(self):
        return self.ax.get_title()

    def get_actions(self):
        actions = self.toolbar.actions()
        return actions

    def inspect(self):
        pass

    def show_colorbar(self, show = None):
        if show is not None:
            self.colorbar_visible = show
        if self.colorbar_visible:
            if not self.colorbar:
                self.set_colorbar()
        else:
            self.remove_colorbar()
        self.draw()

    def remove_colorbar(self):
        if self.colorbar is not None:
            self.colorbar.remove()
            self.colorbar = None

    def set_colorbar(self):
        self.colorbar = self.figure.colorbar(self.cax, orientation = "horizontal", pad = 0.2)
        self.colorbar.ax.tick_params(labelsize=7)

    def show_labels(self, show = None):
        if show is not None:
            self.labels_visible = show
        if self.labels_visible:
            self.set_labels()
        else:
            self.hide_labels()
        self.draw()

    def set_labels(self, title = None, binary_values = None):
        if binary_values is not None:
            self.binary_values = [float_to_string(value) for value in binary_values]
        if title is not None:
            self.title = title
        self.ax.set_title(self.title)
        self.ax.tick_params(top = False, bottom = True, labeltop = False, labelbottom = True)
        self.ax.set_xticks(np.arange(len(self.node_labels)))
        self.ax.set_yticks(np.arange(len(self.binary_values)))
        self.ax.set_xticklabels(self.node_labels)
        self.ax.set_yticklabels(self.binary_values)
        plt.setp(self.ax.get_xticklabels(), rotation = 90, ha = "right", va = 'center', rotation_mode = "anchor", fontsize = 7)
        plt.setp(self.ax.get_yticklabels(), fontsize = 7)

        self.ax.set_ylabel(self.y_label)
        self.ax.set_xlabel('Brain region')

    def hide_labels(self):
        self.ax.set_xticks(np.array([]))
        self.ax.set_yticks(np.array([]))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_ylabel('')
        self.ax.set_xlabel('')
        self.ax.set_title('')




