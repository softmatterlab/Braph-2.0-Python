from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from braphy.gui.widgets.binary_plot_settings_widget import BinaryPlotSettingsWidget
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import numpy as np

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
        self.confidence_intervals = {}

        self.toolbar = NavigationToolbar(self, self)
        self.toolbar.set_callback_function(self.settings_callback)
        self.toolbar.hide()

    def settings_callback(self):
        self.show_legend(self.ax.get_legend())
        self.draw()

    def add_plot(self, info_string, values, confidence_interval = None):
        settings = self.binary_plot_settings_widget.get_plot_settings()

        values = values[np.argsort(values[:,0])]

        if confidence_interval is not None:
            CI = self.ax.fill_between(values[:, 0], confidence_interval[0], confidence_interval[1],
                                      facecolor = settings['ci_color'],
                                      alpha = settings['ci_alpha'])
            self.confidence_intervals[info_string] = CI
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
        if info_string in self.confidence_intervals.keys():
            self.confidence_intervals[info_string].remove()
            del self.confidence_intervals[info_string]
        self.ax.relim()
        self.ax.autoscale_view()
        self.show_legend(self.ax.get_legend())
        self.draw()

    def resizeEvent(self, event):
        try:
            super().resizeEvent(event)
        except:
            pass
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
        for ci in self.confidence_intervals.values():
            ci.set_facecolor(settings['ci_color'])
            ci.set_alpha(settings['ci_alpha'])
        self.show_legend(self.ax.get_legend())
        self.draw()

    def clear_plot(self):
        for plot in self.plots.values():
            plot[0].remove()
        for confidence_interval in self.confidence_intervals.values():
            confidence_interval.remove()
        self.plots = {}
        self.confidence_intervals = {}
        self.show_legend(False)
        self.draw()

    def show_legend(self, show):
        if show:
            self.ax.legend()
            self.parent().parent().actionLegend.blockSignals(True)
            self.parent().parent().actionLegend.setChecked(True)
            self.parent().parent().actionLegend.blockSignals(False)
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



