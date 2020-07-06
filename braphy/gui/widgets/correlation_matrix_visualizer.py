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
        fig.canvas.mpl_connect("button_press_event", self.inspect)
        self.text = None
        self.matrix = None
        self.mouse_mode_inspect = False
        self.labels = []
        self.labels_visible = False
        self.colorbar_visible = False
        self.lines = []

    def init(self, matrix):
        self.matrix = matrix
        self.plot()

    def update_matrix(self, matrix, histogram = False):
        if self.matrix is None:
            self.init(matrix)
        else:
            self.matrix = matrix
            if histogram:
                self.histogram()
            else:
                if self.cax is None:
                    self.plot()
                else:
                    self.cax.set_data(self.matrix)
                    self.draw()

    def set_labels(self, labels):
        self.labels = labels
        self.show_labels(self.labels_visible)

    def plot(self):
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.cax = self.ax.imshow(self.matrix, vmin = 0, vmax = 1)
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

    def divide_communities(self, state, regions = []):
        if len(regions) > 0:
            regions.sort()
        if state:
            offset = 0.5
            for i in range(int(max(regions) + 1)):
                start_coord = np.where(regions == i)[0][0] - offset
                end_coord = np.where(regions == i)[0][-1] + offset
                self.draw_rectangle(start_coord, end_coord)
        else:
            for line in self.lines:
                line[0].remove()
            self.lines = []
            self.draw()

    def draw_rectangle(self, start_coord, end_coord):
        self.draw_line([start_coord, start_coord], [start_coord, end_coord])
        self.draw_line([start_coord, end_coord], [start_coord, start_coord])
        self.draw_line([start_coord, end_coord], [end_coord, end_coord])
        self.draw_line([end_coord, end_coord], [start_coord, end_coord])

    def draw_line(self, x, y):
        line = self.ax.plot(x, y, color='black', linewidth=2)
        self.lines.append(line)
        self.draw()

    def histogram(self):
        self.figure.clear()
        self.ax.clear()
        self.colorbar_visible = False
        self.show_colorbar(True)
        self.show_labels(True)
        self.ax = self.figure.add_subplot(111)
        self.ax.hist(self.matrix.flatten())
        self.cax = None
        self.draw()
        self.show_colorbar(False)

    def show_labels(self, show):
        if self.labels_visible == show:
            return
        self.labels_visible = show
        if show:
            if len(self.labels) != self.matrix.shape[0]:
                self.labels = ['region']*self.matrix.shape[0]
            self.ax.set_xticks(np.arange(len(self.matrix)))
            self.ax.set_yticks(np.arange(len(self.matrix)))
            self.ax.set_xticklabels(self.labels)
            self.ax.set_yticklabels(self.labels)
        else:
            self.ax.set_xticks(np.array([]))
            self.ax.set_yticks(np.array([]))
            self.ax.set_xticklabels([])
            self.ax.set_yticklabels([])
        self.draw()

    def show_colorbar(self, show):
        if self.colorbar_visible == show:
            return
        self.colorbar_visible = show
        if show:
            self.colorbar = self.figure.colorbar(self.cax)
        else:
            self.colorbar.remove()
        self.draw()

    def save_fig(self, file_name):
        self.figure.savefig(file_name)

    def inspect(self, event):
        if self.mouse_mode_inspect:
            if event.xdata and event.ydata:
                self.clear_text()
                x = int(round(event.xdata))
                y = int(round(event.ydata))
                tool_tip_label = "x: {}\ny: {}\nz: {}".format(x, y, self.matrix[y, x])
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                self.text = self.ax.text((event.xdata+0.5)/len(self.matrix),1-(event.ydata+0.5)/len(self.matrix), tool_tip_label, transform=self.ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
                self.draw()

    def clear_text(self):
        if self.text:
            self.text.remove()
            self.text = None

