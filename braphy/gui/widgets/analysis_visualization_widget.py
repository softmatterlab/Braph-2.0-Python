from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets, Qt
from pyqtgraph import ColorMap as cm
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative, float_to_string
from braphy.gui.color_bar_combo_box import ColorBar

ui_file = abs_path_from_relative(__file__, "../ui_files/measure_visualization_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class AnalysisVisualizationWidget(Base, Form):
    def __init__(self, parent = None):
        super(AnalysisVisualizationWidget, self).__init__(parent)
        self.setupUi(self)
        self.visualization_options = ['Color', 'Size', 'Color and size']
        self.colormaps = self.get_colormaps()

    def init(self, settings_widget, groups, binary_type):
        self.binary_type = binary_type
        self.init_combo_boxes(groups)
        self.brain_widget = settings_widget.brain_widget
        self.settings_widget = settings_widget
        self.update_list()
        self.visualization_type_changed(0)
        self.init_spin_boxes()
        self.listWidget.currentRowChanged.connect(self.list_item_changed)
        if self.binary_type:
            self.labelBinary.setText(binary_type)
        else:
            self.labelBinary.hide()
            self.comboBoxBinary.hide()
        self.comboBoxBinary.setEnabled(False)

    def init_combo_boxes(self, groups):
        for group in groups:
            self.comboBoxGroup.addItem(group.name)
            self.comboBoxGroup2.addItem(group.name)
        self.comboBoxGroup.currentIndexChanged.connect(self.group_changed)
        self.comboBoxGroup2.currentIndexChanged.connect(self.group_changed)
        self.comboBoxColormap.reset()
        for colormap in self.colormaps.values():
            self.comboBoxColormap.add_colormap(colormap)
        self.comboBoxColormap.setCurrentIndex(0)
        self.comboBoxColormap.currentIndexChanged.connect(self.update_visualization)
        self.comboBoxBinary.currentIndexChanged.connect(self.update_visualization)

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
        self.update_list()
        self.update_binary_values()
        self.update_visualization()

    def update_binary_values(self):
        pass

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

class MeasureVisualizationWidget(AnalysisVisualizationWidget):
    def __init__(self, parent = None):
        super(MeasureVisualizationWidget, self).__init__(parent)
        self.checkBoxDiff.hide()
        self.checkBoxSingle.hide()
        self.checkBoxDouble.hide()
        self.comboBoxDiff.hide()
        self.comboBoxSingle.hide()
        self.comboBoxDouble.hide()
        self.comboBoxGroup2.hide()
        self.comboBoxColormap.setEnabled(False)

    def init(self, settings_widget, measurements, groups, binary_type):
        self.measurements = measurements
        super().init(settings_widget, groups, binary_type)

    def init_combo_boxes(self, groups):
        super().init_combo_boxes(groups)
        self.comboBoxType.addItems(self.visualization_options)
        self.comboBoxType.currentIndexChanged.connect(self.visualization_type_changed)
        self.comboBoxType.setEnabled(False)
        self.comboBoxColormap.setEnabled(False)

    def update_list(self):
        group_index = self.comboBoxGroup.currentIndex()
        self.listWidget.clear()
        self.listWidget.blockSignals(True)
        self.measure_mapping = {}
        for i, measurement in enumerate(self.measurements):
            is_nodal = measurement.is_nodal()
            items = self.listWidget.findItems(measurement.sub_measure, Qt.Qt.MatchExactly)
            items_text = [item.text() for item in items]
            if (measurement.group == group_index and
                is_nodal and
                measurement.sub_measure not in items_text):
                self.listWidget.addItem(measurement.sub_measure)
                self.measure_mapping[measurement.sub_measure] = i
        self.listWidget.blockSignals(False)

    def list_item_changed(self, index):
        enabled = True if index > -1 else False
        items = [self.comboBoxType, self.comboBoxColormap, self.labelMin, self.labelMax, self.spinBoxMin, self.spinBoxMax]
        if enabled:
            self.labelBinary.setEnabled(True)
            self.comboBoxBinary.setEnabled(True)
            for item in items:
                item.setEnabled(True)
        else:
            self.labelBinary.setEnabled(False)
            self.comboBoxBinary.setEnabled(False)
            for item in items:
                item.setEnabled(False)
        if self.binary_type:
            self.update_binary_values()
        self.update_visualization()

    def update_binary_values(self):
        self.comboBoxBinary.blockSignals(True)
        if self.listWidget.currentRow() == -1:
            self.comboBoxBinary.blockSignals(False)
            return
        group_index = self.comboBoxGroup.currentIndex()
        self.comboBoxBinary.clear()
        self.binary_mapping = []
        current_list_item = self.listWidget.currentItem().text()
        for i, measurement in enumerate(self.measurements):
            if (measurement.sub_measure == current_list_item and
                measurement.group == group_index):
                self.binary_mapping.append(i)
                self.comboBoxBinary.addItem(float_to_string(measurement.binary_value))
        self.comboBoxBinary.blockSignals(False)

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
        if self.binary_type and self.comboBoxBinary.currentIndex == -1:
            return
        values = self.get_visualization_values()
        visualization_type = self.comboBoxType.currentIndex()
        for i, region in enumerate(self.brain_widget.gui_brain_regions):
            if np.isnan(values[i]) or np.isinf(values[i]):
                region.set_size(0.1)
                continue
            if visualization_type == 0 or visualization_type == 2:
                region.set_color(self.get_color(values[i]))
            if visualization_type == 1 or visualization_type == 2:
                region.set_size(values[i] * self.spinBoxMax.value() + self.spinBoxMin.value())

    def get_visualization_values(self):
        if self.binary_type:
            binary_index = self.comboBoxBinary.currentIndex()
            measurement_index = self.binary_mapping[binary_index]
        else:
            current_list_item = self.listWidget.currentItem().text()
            measurement_index = self.measure_mapping[current_list_item]
        measurement = self.measurements[measurement_index]
        values = measurement.value
        if isinstance(values[0], np.ndarray): # fmri: compute average
            values = np.mean(values, axis = 0)
        values = self.normalize(values)
        return values

class MeasureComparisonVisualizationWidget(AnalysisVisualizationWidget):
    def __init__(self, parent = None):
        super(MeasureComparisonVisualizationWidget, self).__init__(parent)
        self.visualization_options = ['Color', 'Size']
        self.label.hide()
        self.comboBoxType.hide()
        self.init_check_boxes()

    def init(self, settings_widget, comparisons, groups, binary_type):
        self.comparisons = comparisons
        super().init(settings_widget, groups, binary_type)

    def init_check_boxes(self):
        self.checkBoxDiff.stateChanged.connect(self.visualize_difference)
        self.checkBoxSingle.stateChanged.connect(self.visualize_single)
        self.checkBoxDouble.stateChanged.connect(self.visualize_double)
        self.checkBoxDiff.setEnabled(False)
        self.checkBoxSingle.setEnabled(False)
        self.checkBoxDouble.setEnabled(False)

    def init_combo_boxes(self, groups):
        super().init_combo_boxes(groups)
        combo_boxes = [self.comboBoxDiff, self.comboBoxSingle, self.comboBoxDouble]
        for combo_box in combo_boxes:
            combo_box.addItems(self.visualization_options)
            combo_box.currentIndexChanged.connect(lambda index, combo_box = combo_box: self.set_combo_box_visualization(index, combo_box))
            combo_box.setEnabled(False)
            combo_box.blockSignals(True)
            combo_box.setCurrentIndex(-1)
            combo_box.blockSignals(False)

    def disable_check_boxes(self):
        check_boxes = [self.checkBoxDiff, self.checkBoxSingle, self.checkBoxDouble]
        number_of_checked_boxes = sum([box.isChecked() for box in check_boxes])
        for box in check_boxes:
            box.setEnabled(True)
            if number_of_checked_boxes >= 2:
                if not box.isChecked():
                    box.setEnabled(False)
        self.visualization_type_changed()

    def set_combo_box_visualization(self, index, combo_box):
        combo_boxes = [self.comboBoxDiff, self.comboBoxSingle, self.comboBoxDouble]
        for box in combo_boxes:
            if box == combo_box:
                continue
            if box.currentIndex() == index:
                box.blockSignals(True)
                box.setCurrentIndex(-1)
                box.blockSignals(False)
        self.visualization_type_changed()

    def visualize_difference(self, state):
        self.comboBoxDiff.setEnabled(state)
        self.disable_check_boxes()

    def visualize_single(self, state):
        self.comboBoxSingle.setEnabled(state)
        self.disable_check_boxes()

    def visualize_double(self, state):
        self.comboBoxDouble.setEnabled(state)
        self.disable_check_boxes()

    def update_list(self):
        group_index_0 = self.comboBoxGroup.currentIndex()
        group_index_1 = self.comboBoxGroup2.currentIndex()
        self.listWidget.clear()
        self.listWidget.blockSignals(True)
        self.comparison_mapping = {}
        for i, comparison in enumerate(self.comparisons):
            is_nodal = comparison.measure_class.is_nodal(comparison.sub_measure)
            items = self.listWidget.findItems(comparison.sub_measure, Qt.Qt.MatchExactly)
            items_text = [item.text() for item in items]
            if (comparison.groups[0] == group_index_0 and
                comparison.groups[1] == group_index_1 and
                is_nodal and
                comparison.sub_measure not in items_text):
                self.listWidget.addItem(comparison.sub_measure)
                self.comparison_mapping[comparison.sub_measure] = i
        self.listWidget.blockSignals(False)

    def list_item_changed(self, index):
        enabled = True if index > -1 else False
        if enabled:
            self.disable_check_boxes()
            self.comboBoxBinary.setEnabled(True)
        else:
            self.comboBoxBinary.setEnabled(False)
            self.update_binary_values()
            check_boxes = [self.checkBoxDiff, self.checkBoxSingle, self.checkBoxDouble]
            for check_box in check_boxes:
                check_box.blockSignals(True)
                check_box.setChecked(False)
                check_box.setEnabled(False)
                check_box.blockSignals(False)
            combo_boxes = [self.comboBoxDiff, self.comboBoxSingle, self.comboBoxDouble]
            for combo_box in combo_boxes:
                combo_box.setEnabled(False)
            self.comboBoxColormap.setEnabled(False)
            self.spinBoxMin.setEnabled(False)
            self.spinBoxMax.setEnabled(False)
            self.labelMin.setEnabled(False)
            self.labelMax.setEnabled(False)
        if self.binary_type:
            self.update_binary_values()
        self.update_visualization()

    def update_binary_values(self):
        self.comboBoxBinary.blockSignals(True)
        self.comboBoxBinary.clear()
        if self.listWidget.currentRow() == -1:
            self.comboBoxBinary.blockSignals(False)
            return
        group_index_0 = self.comboBoxGroup.currentIndex()
        group_index_1 = self.comboBoxGroup2.currentIndex()
        self.comboBoxBinary.clear()
        self.binary_mapping = []
        current_list_item = self.listWidget.currentItem().text()
        for i, comparison in enumerate(self.comparisons):
            if (comparison.sub_measure == current_list_item and
                comparison.groups[0] == group_index_0 and
                comparison.groups[1] == group_index_1):
                self.binary_mapping.append(i)
                self.comboBoxBinary.addItem(float_to_string(comparison.binary_value))
        self.comboBoxBinary.blockSignals(False)

    def visualization_type_changed(self, index = 0):
        self.spinBoxMin.setEnabled(False)
        self.spinBoxMax.setEnabled(False)
        self.labelMin.setEnabled(False)
        self.labelMax.setEnabled(False)
        self.comboBoxColormap.setEnabled(False)
        combo_boxes = [self.comboBoxDiff, self.comboBoxSingle, self.comboBoxDouble]
        for combo_box in combo_boxes:
            if combo_box.isEnabled():
                current_index = combo_box.currentIndex()
                if current_index == 0: # color
                    self.comboBoxColormap.setEnabled(True)
                elif current_index == 1: # size
                    self.spinBoxMin.setEnabled(True)
                    self.spinBoxMax.setEnabled(True)
                    self.labelMin.setEnabled(True)
                    self.labelMax.setEnabled(True)
        self.update_visualization()

    def update_visualization(self):
        self.brain_widget.reset_brain_region_colors()
        self.settings_widget.change_brain_region_size()
        if self.listWidget.currentRow() == -1:
            return
        if self.binary_type and self.comboBoxBinary.currentIndex == -1:
            return
        for i, region in enumerate(self.brain_widget.gui_brain_regions):
            if self.checkBoxDiff.isChecked():
                values = self.get_visualization_values('diff')
                if self.comboBoxDiff.currentIndex() == 0:
                    region.set_color(self.get_color(values[i]))
                elif self.comboBoxDiff.currentIndex() == 1:
                    region.set_size(values[i] * self.spinBoxMax.value() + self.spinBoxMin.value())
            if self.checkBoxSingle.isChecked():
                values = self.get_visualization_values('single')
                if self.comboBoxSingle.currentIndex() == 0:
                    region.set_color(self.get_color(values[i]))
                elif self.comboBoxSingle.currentIndex() == 1:
                    region.set_size(values[i] * self.spinBoxMax.value() + self.spinBoxMin.value())
            if self.checkBoxDouble.isChecked():
                values = self.get_visualization_values('double')
                if self.comboBoxDouble.currentIndex() == 0:
                    region.set_color(self.get_color(values[i]))
                elif self.comboBoxDouble.currentIndex() == 1:
                    region.set_size(values[i] * self.spinBoxMax.value() + self.spinBoxMin.value())

    def get_visualization_values(self, type):
        if self.binary_type:
            binary_index = self.comboBoxBinary.currentIndex()
            comparison_index = self.binary_mapping[binary_index]
        else:
            current_list_item = self.listWidget.currentItem().text()
            comparison_index = self.comparison_mapping[current_list_item]
        comparison = self.comparisons[comparison_index]
        if type == 'diff':
            values_0 = comparison.measures[0]
            values_1 = comparison.measures[1]
            if isinstance(values_0[0], np.ndarray):
                values_0 = np.mean(values_0, axis = 0)
                values_1 = np.mean(values_1, axis = 0)
            values = values_0 - values_1
        elif type == 'single':
            values = comparison.p_values[0]
        elif type == 'double':
            values = comparison.p_values[1]
        values = self.normalize(values)
        return values
