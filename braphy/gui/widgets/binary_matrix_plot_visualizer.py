from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from braphy.utility.math_utility import float_to_string

class BinaryMatrixPlotVisualizer(FigureCanvas):
    def __init__(self, parent = None, width = 8, height = 6, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.binary_values = None

    def init(self, node_labels):
        self.node_labels = node_labels

    def plot(self, matrix, title = None, binary_values = None):
        if binary_values is not None:
            self.binary_values = binary_values
        if title is None:
            title = self.ax.get_title()
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.cax = self.ax.imshow(matrix)

        self.ax.tick_params(top = False, bottom = True, labeltop = False, labelbottom = True)
        plt.setp(self.ax.get_xticklabels(), rotation = 90, ha = "right", rotation_mode = "anchor", fontsize = 7)
        plt.setp(self.ax.get_yticklabels(), fontsize = 7)
        binary_values = [float_to_string(value) for value in self.binary_values]
        self.ax.set_xticks(np.arange(len(self.node_labels)))
        self.ax.set_yticks(np.arange(len(binary_values)))
        self.ax.set_xticklabels(self.node_labels)
        self.ax.set_yticklabels(binary_values)

        self.ax.set_ylabel('Binary value')
        self.ax.set_xlabel('Node')
        self.ax.set_title(title)

        self.colorbar = self.figure.colorbar(self.cax, orientation = "horizontal", pad = 0.2)
        self.colorbar.ax.tick_params(labelsize=7)

        self.figure.tight_layout()
        self.draw()

    def get_title(self):
        return self.ax.get_title()



