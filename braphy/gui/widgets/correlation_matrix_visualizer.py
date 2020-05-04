from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import math
import random

class CorrelationMatrixVisualizer(FigureCanvas):
    MOUSE_MODE_ZOOM_IN = 1
    MOUSE_MODE_ZOOM_OUT = 2
    MOUSE_MODE_PAN = 3
    MOUSE_MODE_INSPECT = 4
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        fig.canvas.mpl_connect("button_press_event", self.onclick)
        self.text = None
        self.mouse_mode = None

    def init(self, matrix):
        self.matrix = matrix
        self.plot()

    def plot(self):
        self.ax = self.figure.add_subplot(111)
        self.cax = self.ax.matshow(self.matrix)
        self.show_colorbar(True)
        self.show_labels(True)
        self.ax.tick_params(top=False, bottom=True,
                            labeltop=False, labelbottom=True)
        plt.setp(self.ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor", fontsize = 7)
        plt.setp(self.ax.get_yticklabels(), fontsize = 7)
        self.figure.tight_layout()
        self.draw()
        self.show_labels(False)
        self.show_colorbar(False)

    def show_labels(self, show):
        if show:
            self.ax.set_xticks(np.arange(len(self.matrix)))
            self.ax.set_yticks(np.arange(len(self.matrix)))
            self.ax.set_xticklabels(['region']*len(self.matrix))
            self.ax.set_yticklabels(['region']*len(self.matrix))
        else:
            self.ax.set_xticks(np.array([]))
            self.ax.set_yticks(np.array([]))
            self.ax.set_xticklabels([])
            self.ax.set_yticklabels([])
        self.draw()

    def show_colorbar(self, show):
        if show:
            self.colorbar = self.figure.colorbar(self.cax)
        else:
            self.colorbar.remove()
        self.draw()

    def save_fig(self, file_name):
        self.figure.savefig(file_name)

    def onclick(self, event):
        if self.mouse_mode == CorrelationMatrixVisualizer.MOUSE_MODE_ZOOM_IN:
            self.zoom_in(event)
        elif self.mouse_mode == CorrelationMatrixVisualizer.MOUSE_MODE_ZOOM_OUT:
            self.zoom_out(event)
        elif self.mouse_mode == CorrelationMatrixVisualizer.MOUSE_MODE_PAN:
            self.pan(event)
        elif self.mouse_mode == CorrelationMatrixVisualizer.MOUSE_MODE_INSPECT:
            self.inspect(event)

    def zoom_in(self, event):
        if event.xdata and event.ydata:
            x = int(round(event.xdata))
            y = int(round(event.ydata))
            size = self.ax.get_xlim()[1] - self.ax.get_xlim()[0]
            if size <= 3:
                return
            new_size = math.ceil(size/2)
            x = min(x, size - int(new_size/2))
            x = max(x, int(new_size/2))
            y = min(y, size - int(new_size/2))
            y = max(y, int(new_size/2))
            x_min = x - int(new_size/2)
            x_max = x + int(new_size/2)
            y_min = y - int(new_size/2)
            y_max = y + int(new_size/2)
            self.ax.set_xlim([x_min-0.5, x_max+0.5])
            self.ax.set_ylim([y_max+0.5, y_min-0.5])
            self.draw()

    def zoom_out(self, event):
        pass

    def pan(self, event):
        pass

    def inspect(self, event):
        pass

    def inspect(self, event):
        if event.xdata and event.ydata:
            if self.text:
                self.text.remove()
            x = int(round(event.xdata))
            y = int(round(event.ydata))
            tool_tip_label = "x: {}\ny: {}\nz: {}".format(x, y, self.matrix[x, y])
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            self.text = self.ax.text((event.xdata+0.5)/len(self.matrix),1-(event.ydata+0.5)/len(self.matrix), tool_tip_label, transform=self.ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
            self.draw()
