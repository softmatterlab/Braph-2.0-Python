from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import math
import random

class CorrelationMatrixVisualizer(FigureCanvas):
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
        if event.xdata and event.ydata:
            if self.text:
                self.text.remove()
            x = int(round(event.xdata))
            y = int(round(event.ydata))
            tool_tip_label = "x: {}\ny: {}\nz: {}".format(x, y, self.matrix[x, y])
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            self.text = self.ax.text((event.xdata+0.5)/len(self.matrix),1-(event.ydata+0.5)/len(self.matrix), tool_tip_label, transform=self.ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
            self.draw()
