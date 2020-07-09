from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from braphy.gui.widgets.binary_plot_settings_widget import BinaryPlotSettingsWidget
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import math
import random

class BinaryPlotVisualizer(FigureCanvas):
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.binary_plot_settings_widget = BinaryPlotSettingsWidget(parent = self, update_function = self.update_visualization)
        self.binary_plot_settings_widget.raise_()
        self.binary_plot_settings_widget.show()

        self.plots = {}


    def add_plot(self, info_string, values):
        self.figure.clear()
        settings = self.binary_plot_settings_widget.get_plot_settings()
        self.ax = self.figure.add_subplot(111)
        plot = self.ax.plot(values[:, 0], values[:, 1], color = settings['line_color'],
                            linestyle = settings['line_style'], marker = settings['marker_style'],
                            markerfacecolor = settings['marker_color'])
        print(len(plot))
        self.plots[info_string] = plot

        self.ax.tick_params(top=False, bottom=True,
                            labeltop=False, labelbottom=True)
        plt.setp(self.ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor", fontsize = 7)
        plt.setp(self.ax.get_yticklabels(), fontsize = 7)
        self.figure.tight_layout()
        self.draw()

    def remove_plot(self, info_string):
        self.plots[info_string][0].remove()
        del self.plots[info_string]
        self.draw()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.binary_plot_settings_widget.update_move()

    def update_visualization(self):
        settings = self.binary_plot_settings_widget.get_plot_settings()
        for plot in self.plots.values():
            plot[0].set_color(settings['line_color'])
            plot[0].set_linestyle(settings['line_style'])
            plot[0].set_marker(settings['marker_style'])
            plot[0].set_markerfacecolor(settings['marker_color'])
            plot[0].set_markersize(settings['marker_size'])
            plot[0].set_linewidth(settings['line_width'])
        self.draw()


