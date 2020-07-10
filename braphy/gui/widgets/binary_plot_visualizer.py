from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from braphy.gui.widgets.binary_plot_settings_widget import BinaryPlotSettingsWidget
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import math
import random
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

class NavigationToolbar(NavigationToolbar2QT):
    def edit_parameters(self):
        super(NavigationToolbar, self).edit_parameters()
        self.callback_function()

    def set_callback_function(self, callback_function):
        self.callback_function = callback_function

class BinaryPlotVisualizer(FigureCanvas):
    def __init__(self, parent = None, width = 8, height = 6, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        self.ax.set_ylabel('Value')
        self.ax.set_title(' ')
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

        self.toolbar = NavigationToolbar(self, self)
        self.toolbar.set_callback_function(self.settings_callback)
        self.toolbar.hide()

    def settings_callback(self):
        self.show_legend(self.ax.get_legend())
        self.draw()

    def add_plot(self, info_string, values):
        settings = self.binary_plot_settings_widget.get_plot_settings()
        
        plot = self.ax.plot(values[:, 0], values[:, 1], color = settings['line_color'],
                            linestyle = settings['line_style'], marker = settings['marker_style'],
                            markerfacecolor = settings['marker_color'], linewidth = settings['line_width'],
                            markersize = settings['marker_size'], label = info_string)
        self.plots[info_string] = plot
        self.ax.tick_params(top = False, bottom = True, labeltop = False, labelbottom = True)
        plt.setp(self.ax.get_xticklabels(), fontsize = 7)
        plt.setp(self.ax.get_yticklabels(), fontsize = 7)
        self.figure.tight_layout()
        self.ax.relim()
        self.ax.autoscale_view()
        self.show_legend(self.ax.get_legend())
        self.draw()

    def remove_plot(self, info_string):
        self.plots[info_string][0].remove()
        del self.plots[info_string]
        self.ax.relim()
        self.ax.autoscale_view()
        self.show_legend(self.ax.get_legend())
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
        self.show_legend(self.ax.get_legend())
        self.draw()

    def clear_plot(self):
        self.ax.cla()
        self.plots = {}
        self.draw()

    def show_legend(self, show):
        if show:
            self.ax.legend()
            self.parent().actionLegend.blockSignals(True)
            self.parent().actionLegend.setChecked(True)
            self.parent().actionLegend.blockSignals(False)
        else:
            legend = self.ax.get_legend()
            if legend:
                legend.remove()
        self.draw()

    def set_x_label(self, label):
        self.ax.set_xlabel(label)

    def get_actions(self):
        actions = self.toolbar.actions()
        return actions



