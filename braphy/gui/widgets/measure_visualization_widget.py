from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from pyqtgraph import ColorMap as cm
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.gui.color_bar_combo_box import ColorBar

ui_file = abs_path_from_relative(__file__, "../ui_files/measure_visualization_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class MeasureVisualizationWidget(Base, Form):
    def __init__(self, parent = None):
        super(MeasureVisualizationWidget, self).__init__(parent)
        self.setupUi(self)
        self.visualization_options = ['Color', 'Size', 'Color and size']
        self.colormaps = self.get_colormaps()

    def init(self, settings_widget, measurements, groups):
        self.measurements = measurements
        self.init_combo_boxes(groups)
        self.brain_widget = settings_widget.brain_widget
        self.settings_widget = settings_widget

    def init_combo_boxes(self, groups):
        self.comboBoxType.addItems(self.visualization_options)
        self.comboBoxType.currentIndexChanged.connect(self.update_visualization)
        for group in groups:
            self.comboBoxGroup.addItem(group.name)
        self.comboBoxGroup.currentIndexChanged.connect(self.group_changed)
        self.comboBoxBinary.currentIndexChanged.connect(self.update_visualization)

        self.comboBoxColormap.reset()
        for colormap in self.colormaps.values():
            self.comboBoxColormap.add_colormap(colormap)
        self.comboBoxColormap.setCurrentIndex(0)
        self.comboBoxColormap.currentIndexChanged.connect(self.update_visualization)

    def group_changed(self, group_index):
        self.update_list(group_index)
        self.update_binary_values(group_index)
        self.update_visualization()

    def update_list(self, group_index):
        self.listWidget.blockSignals(True)
        self.listWidget.clear()
        self.measure_mapping = {}
        for i, measurement in enumerate(self.measurements):
            if measurement.group == group_index:
                self.listWidget.additem(measurement.sub_measure)
                self.measure_mapping[measurement.sub_measure] = i
        self.listWidget.blockSignals(False)

    def update_binary_values(self, group_index):
        pass

    def update_visualization(self):
        pass

    def get_colormaps(self):
        colormaps = {}
        colormaps['spring'] = cm([0.0, 1.0], [[1.0, 0.28, 0.85, 1.0], [1.0, 0.94, 0.28, 1.0]])
        colormaps['cool'] = cm([0.0, 1.0], [[0.298, 0.964, 0.956, 1.0], [1.0, 0.28, 0.85, 1.0]])
        colormaps['hot'] = cm([0.0, 0.33, 0.67, 1.0], [[0.0, 0.0, 0.0, 1.0], [1.0, 0.0, 0.0, 1.0], [1.0, 1.0, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0]])
        colormaps['parula'] = cm([0.0, 0.5, 1.0], [[0.317, 0.223, 0.937, 1.0], [0.333, 0.666, 0.5, 1.0], [1.0, 0.94, 0.28, 1.0]])
        return colormaps