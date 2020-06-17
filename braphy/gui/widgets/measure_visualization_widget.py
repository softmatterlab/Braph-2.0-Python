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
        self.checkBoxDiff.hide()
        self.checkBoxSingle.hide()
        self.checkBoxDouble.hide()
        self.comboBoxDiff.hide()
        self.comboBoxSingle.hide()
        self.comboBoxDouble.hide()
        self.comboBoxGroup2.hide()

    def init(self, settings_widget, measurements, groups):
        self.measurements = measurements
        self.init_combo_boxes(groups)
        self.brain_widget = settings_widget.brain_widget
        self.settings_widget = settings_widget
        self.update_list(0)
        self.visualization_type_changed(0)
        self.listWidget.currentTextChanged.connect(self.update_visualization)
        self.init_spin_boxes()

    def init_combo_boxes(self, groups):
        self.comboBoxType.addItems(self.visualization_options)
        self.comboBoxType.currentIndexChanged.connect(self.visualization_type_changed)
        for group in groups:
            self.comboBoxGroup.addItem(group.name)
        self.comboBoxGroup.currentIndexChanged.connect(self.group_changed)
        self.comboBoxBinary.currentIndexChanged.connect(self.update_visualization)

        self.comboBoxColormap.reset()
        for colormap in self.colormaps.values():
            self.comboBoxColormap.add_colormap(colormap)
        self.comboBoxColormap.setCurrentIndex(0)
        self.comboBoxColormap.currentIndexChanged.connect(self.update_visualization)

    def init_spin_boxes(self):
        self.spinBoxMin.setValue(1)
        self.spinBoxMax.setValue(10)
        self.spinBoxMin.valueChanged.connect(self.spin_box_min_changed)
        self.spinBoxMax.valueChanged.connect(self.spin_box_max_changed)

    def spin_box_min_changed(self, value):
        self.spinBoxMax.setMinimum(value)
        if self.spinBoxMax.value() < value:
            self.spinBoxMax.blockSignals(True)
            self.spinBoxMax.setValue(value)
            self.spinBoxMax.blockSignals(False)
        self.update_visualization()

    def spin_box_max_changed(self, value):
        self.spinBoxMin.setMaximum(value)
        if self.spinBoxMin.value() > value:
            self.spinBoxMin.blockSignals(True)
            self.spinBoxMin.setValue(value)
            self.spinBoxMin.blockSignals(False)
        self.update_visualization()

    def group_changed(self, group_index):
        self.update_list(group_index)
        self.update_binary_values(group_index)
        self.update_visualization()

    def update_list(self, group_index):
        self.listWidget.blockSignals(True)
        self.listWidget.clear()
        self.measure_mapping = {}
        for i, measurement in enumerate(self.measurements):
            if measurement.group == group_index and measurement.is_nodal():
                self.listWidget.addItem(measurement.sub_measure)
                self.measure_mapping[measurement.sub_measure] = i
        self.listWidget.blockSignals(False)

    def update_binary_values(self, group_index):
        pass

    def visualization_type_changed(self, index):
        if index == 0: # color
            self.spinBoxMin.setEnabled(False)
            self.spinBoxMax.setEnabled(False)
            self.labelMin.setEnabled(False)
            self.labelMax.setEnabled(False)
            self.comboBoxColormap.setEnabled(True)
        elif index == 1: # size
            self.spinBoxMin.setEnabled(True)
            self.spinBoxMax.setEnabled(True)
            self.labelMin.setEnabled(True)
            self.labelMax.setEnabled(True)
            self.comboBoxColormap.setEnabled(False)
        else:
            self.spinBoxMin.setEnabled(True)
            self.spinBoxMax.setEnabled(True)
            self.labelMin.setEnabled(True)
            self.labelMax.setEnabled(True)
            self.comboBoxColormap.setEnabled(True)
        self.update_visualization()

    def update_visualization(self):
        self.brain_widget.reset_brain_region_colors()
        self.settings_widget.change_brain_region_size()
        if self.listWidget.currentRow() == -1:
            return
        values = self.get_visualization_values()
        visualization_type = self.comboBoxType.currentIndex()
        for i, region in enumerate(self.brain_widget.gui_brain_regions):
            if visualization_type == 0 or visualization_type == 2:
                region.set_color(self.get_color(values[i]))
            if visualization_type == 1 or visualization_type == 2:
                region.set_size(values[i] * self.spinBoxMax.value() + self.spinBoxMin.value())

    def get_visualization_values(self):
        current_list_item = self.listWidget.currentItem().text()
        measurement_index = self.measure_mapping[current_list_item]
        measurement = self.measurements[measurement_index]
        values = measurement.value
        if isinstance(values[0], np.ndarray): # fmri: compute average
            values = np.mean(values, axis = 0)
        values = self.normalize(values)
        return values
    
    def normalize(self, array):
        array_min = np.min(array)
        array_max = np.max(array)
        normalized_array = (array - array_min)/(array_max - array_min)
        return normalized_array

    def get_colormaps(self):
        colormaps = {}
        colormaps['spring'] = cm([0.0, 1.0], [[1.0, 0.28, 0.85, 1.0], [1.0, 0.94, 0.28, 1.0]])
        colormaps['cool'] = cm([0.0, 1.0], [[0.298, 0.964, 0.956, 1.0], [1.0, 0.28, 0.85, 1.0]])
        colormaps['hot'] = cm([0.0, 0.33, 0.67, 1.0], [[0.0, 0.0, 0.0, 1.0], [1.0, 0.0, 0.0, 1.0], [1.0, 1.0, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0]])
        colormaps['parula'] = cm([0.0, 0.5, 1.0], [[0.317, 0.223, 0.937, 1.0], [0.333, 0.666, 0.5, 1.0], [1.0, 0.94, 0.28, 1.0]])
        return colormaps

    def get_color(self, value):
        colormap = self.comboBoxColormap.colormap()
        color = colormap.map(value, mode='float')
        return color