from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
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
        self.plot()

    def plot(self):
        a = np.random.rand(68, 68)
        ax = self.figure.add_subplot(111)
        cax = ax.matshow(a)
        self.figure.colorbar(cax)
        ax.set_xticks(np.arange(len(a)))
        ax.set_yticks(np.arange(len(a)))
        ax.set_xticklabels(['region']*len(a))
        ax.set_yticklabels(['region']*len(a))
        ax.tick_params(top=False, bottom=True,
                   labeltop=False, labelbottom=True)
        plt.setp(ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor", fontsize = 7)
        plt.setp(ax.get_yticklabels(), fontsize = 7)
        self.figure.tight_layout()
        self.draw()