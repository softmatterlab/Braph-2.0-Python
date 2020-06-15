from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from pyqtgraph import ColorMap as cm
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.gui.color_bar_combo_box import ColorBar

ui_file = abs_path_from_relative(__file__, "../ui_files/measure_visualization_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class MeasureComparisonVisualizationWidget(Base, Form):
    def __init__(self, parent = None):
        super(MeasureComparisonVisualizationWidget, self).__init__(parent)
        self.setupUi(self)
        self.visualization_options = ['Color', 'Size']
        self.colormaps = self.get_colormaps()
        self.label.hide()
        self.comboBoxType.hide()
        self.init_check_boxes()

    def init(self, settings_widget, comparisons, groups):
        self.comparisons = comparisons
        self.init_combo_boxes(groups)
        self.brain_widget = settings_widget.brain_widget
        self.settings_widget = settings_widget
        self.update_list(0)
        self.visualization_type_changed(0)
        self.listWidget.currentRowChanged.connect(self.list_item_changed)
        self.init_spin_boxes()

    def init_check_boxes(self):
        self.checkBoxDiff.stateChanged.connect(self.visualize_difference)
        self.checkBoxSingle.stateChanged.connect(self.visualize_single)
        self.checkBoxDouble.stateChanged.connect(self.visualize_double)
        self.checkBoxDiff.setEnabled(False)
        self.checkBoxSingle.setEnabled(False)
        self.checkBoxDouble.setEnabled(False)

    def init_combo_boxes(self, groups):
        combo_boxes = [self.comboBoxDiff, self.comboBoxSingle, self.comboBoxDouble]
        for combo_box in combo_boxes:
            combo_box.addItems(self.visualization_options)
            combo_box.currentIndexChanged.connect(lambda index, combo_box = combo_box: self.set_combo_box_visualization(index, combo_box))
            combo_box.setEnabled(False)
            combo_box.setCurrentIndex(-1)

        for group in groups:
            self.comboBoxGroup.addItem(group.name)
            self.comboBoxGroup2.addItem(group.name)
        self.comboBoxGroup.currentIndexChanged.connect(self.group_changed)
        self.comboBoxGroup2.currentIndexChanged.connect(self.group_changed)
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

    def disable_check_boxes(self):
        check_boxes = [self.checkBoxDiff, self.checkBoxSingle, self.checkBoxDouble]
        number_of_checked_boxes = sum([box.isChecked() for box in check_boxes])
        for box in check_boxes:
            box.setEnabled(True)
            if number_of_checked_boxes >= 2:
                if not box.isChecked():
                    box.setEnabled(False)

    def set_combo_box_visualization(self, index, combo_box):
        combo_boxes = [self.comboBoxDiff, self.comboBoxSingle, self.comboBoxDouble]
        for box in combo_boxes:
            if box == combo_box:
                continue
            if box.currentIndex() == index:
                box.blockSignals(True)
                box.setCurrentIndex(-1)
                box.blockSignals(False)
        self.update_visualization()

    def visualize_difference(self, state):
        self.comboBoxDiff.setEnabled(state)
        self.disable_check_boxes()
        self.update_visualization()

    def visualize_single(self, state):
        self.comboBoxSingle.setEnabled(state)
        self.disable_check_boxes()
        self.update_visualization()

    def visualize_double(self, state):
        self.comboBoxDouble.setEnabled(state)
        self.disable_check_boxes()
        self.update_visualization()

    def update_list(self, group_index):
        group_index_0 = self.comboBoxGroup.currentIndex()
        group_index_1 = self.comboBoxGroup2.currentIndex()
        self.listWidget.clear()
        self.listWidget.blockSignals(True)
        self.comparison_mapping = {}
        for i, comparison in enumerate(self.comparisons):
            is_nodal = comparison.measure_class.is_nodal(comparison.sub_measure)
            if comparison.groups[0] == group_index_0 and comparison.groups[1] == group_index_1 and is_nodal:
                self.listWidget.addItem(comparison.sub_measure)
                self.comparison_mapping[comparison.sub_measure] = i
        self.listWidget.blockSignals(False)

    def list_item_changed(self, index):
        enabled = True if index > -1 else False
        if enabled:
            self.disable_check_boxes()
        else:
            check_boxes = [self.checkBoxDiff, self.checkBoxSingle, self.checkBoxDouble]
            for check_box in check_boxes:
                check_box.setEnabled(False)
        self.update_visualization()

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

        return
        self.brain_widget.reset_brain_region_colors()
        self.settings_widget.change_brain_region_size()
        if self.listWidget.currentRow() == -1:
            return
        current_list_item = self.listWidget.currentItem().text()

        measurement_index = self.measure_mapping[current_list_item]
        measurement = self.measurements[measurement_index]
        values = measurement.value

        values_min = np.min(values)
        values_max = np.max(values)
        values = (values - values_min)/(values_max - values_min)
        visualization_type = self.comboBoxType.currentIndex()
        for i, region in enumerate(self.brain_widget.gui_brain_regions):
            if visualization_type == 0 or visualization_type == 2:
                region.set_color(self.get_color(values[i]))
            if visualization_type == 1 or visualization_type == 2:
                region.set_size(values[i] * self.spinBoxMax.value() + self.spinBoxMin.value())

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