from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from pyqtgraph import ColorMap as cm
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.gui.color_bar_combo_box import ColorBar

ui_file = abs_path_from_relative(__file__, "../ui_files/visualization_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class VisualizationWidget(Base, Form):
    def __init__(self, parent = None):
        super(VisualizationWidget, self).__init__(parent)
        self.setupUi(self)
        self.visualization_options = ['Color', 'Size']
        self.colormaps = self.get_colormaps()
        self.combo_boxes = [self.comboBoxAverage, self.comboBoxStd, self.comboBoxSubject, self.comboBoxPvalueSingle,
                            self.comboBoxPvalueDouble]

    def init(self, settings_widget):
        self.init_combo_boxes()
        self.init_check_boxes()
        self.init_list()
        self.init_spin_boxes()
        self.brain_widget = settings_widget.brain_widget
        self.settings_widget = settings_widget

    def init_combo_boxes(self):

        for combo_box in self.combo_boxes:
            combo_box.clear()
            for option in self.visualization_options:
                combo_box.addItem(option)
            combo_box.setCurrentIndex(-1)
            combo_box.setEnabled(False)

        self.comboBoxColormap.reset()
        for colormap in self.colormaps.values():
            self.comboBoxColormap.add_colormap(colormap)
        self.comboBoxColormap.setCurrentIndex(0)

        self.comboBoxAverage.currentIndexChanged.connect(self.set_average_visualization)
        self.comboBoxStd.currentIndexChanged.connect(self.set_std_visualization)
        self.comboBoxSubject.currentIndexChanged.connect(self.update_visualization)
        self.comboBoxPvalueSingle.currentIndexChanged.connect(self.set_p_value_single_visualization)
        self.comboBoxPvalueDouble.currentIndexChanged.connect(self.set_p_value_double_visualization)
        self.comboBoxColormap.currentIndexChanged.connect(self.update_visualization)

    def init_check_boxes(self):
        self.checkBoxAverage.stateChanged.connect(self.visualize_average)
        self.checkBoxStd.stateChanged.connect(self.visualize_std)
        self.checkBoxPvalueSingle.stateChanged.connect(self.visualize_p_value_single)
        self.checkBoxPvalueDouble.stateChanged.connect(self.visualize_p_value_double)
        self.checkBoxAverage.setEnabled(False)
        self.checkBoxStd.setEnabled(False)
        self.checkBoxPvalueSingle.setEnabled(False)
        self.checkBoxPvalueDouble.setEnabled(False)

    def init_list(self):
        self.item_list = []
        self.listWidget.currentRowChanged.connect(self.list_item_changed)
        self.listWidget_2.currentRowChanged.connect(self.list_2_item_changed)

    def set_list(self, item_list):
        self.item_list = item_list
        self.listWidget.blockSignals(True)
        self.listWidget_2.blockSignals(True)
        self.listWidget.clear()
        self.listWidget_2.clear()
        for item in item_list:
            self.listWidget.addItem(self.get_item_string(item))
            self.listWidget_2.addItem(self.get_item_string(item))
        self.listWidget.blockSignals(False)
        self.listWidget_2.blockSignals(False)
        self.list_item_changed(-1)
        self.list_2_item_changed(-1)

    def get_item_string(self, item):
        pass

    def list_item_changed(self, index):
        pass

    def list_2_item_changed(self, index):
        pass

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

    def set_average_visualization(self, index): # combo box
        self.set_combo_box_visualization(index, self.comboBoxAverage)

    def set_std_visualization(self, index): # combo box
        self.set_combo_box_visualization(index, self.comboBoxStd)

    def set_p_value_single_visualization(self, index): #combo box
        self.set_combo_box_visualization(index, self.comboBoxPvalueSingle)

    def set_p_value_double_visualization(self, index): #combo box
        self.set_combo_box_visualization(index, self.comboBoxPvalueDouble)

    def set_combo_box_visualization(self, index, combo_box):
        for box in self.combo_boxes:
            if box == combo_box:
                continue
            if box.currentIndex() == index:
                box.blockSignals(True)
                box.setCurrentIndex(-1)
                box.blockSignals(False)
        self.update_visualization()

    def visualize_average(self, state): # check box
        self.comboBoxAverage.setEnabled(state)
        self.disable_check_boxes()
        self.update_visualization()

    def visualize_std(self, state): # check box
        self.comboBoxStd.setEnabled(state)
        self.disable_check_boxes()
        self.update_visualization()

    def visualize_p_value_single(self, state): # check box
        self.comboBoxPvalueSingle.setEnabled(state)
        self.disable_check_boxes()
        self.update_visualization()

    def visualize_p_value_double(self, state): # check box
        self.comboBoxPvalueDouble.setEnabled(state)
        self.disable_check_boxes()
        self.update_visualization()

    def disable_check_boxes(self):
        check_boxes = [self.checkBoxAverage, self.checkBoxStd, self.checkBoxPvalueSingle, self.checkBoxPvalueDouble]
        number_of_checked_boxes = sum([box.isChecked() for box in check_boxes])
        for box in check_boxes:
            box.setEnabled(True)
            if number_of_checked_boxes >= 2:
                if not box.isChecked():
                    box.setEnabled(False)

    def update_visualization(self):
        self.brain_widget.reset_brain_region_colors()
        self.settings_widget.change_brain_region_size()

    def set_visualization(self, combo_box, values):
        values_min = np.min(values)
        values_max = np.max(values)
        values = (values - values_min)/(values_max - values_min)
        visualization_type = combo_box.currentText()
        for i, region in enumerate(self.brain_widget.gui_brain_regions):
            if visualization_type == 'Color':
                region.set_color(self.get_color(values[i]))
            if visualization_type == 'Size':
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

class SubjectVisualizationWidget(VisualizationWidget):
    def __init_():
        super(VisualizationWidget, self).__init__(parent)

    def init_combo_boxes(self):
        super().init_combo_boxes()
        self.comboBoxAverage.hide()
        self.comboBoxStd.hide()
        self.comboBoxPvalueSingle.hide()
        self.comboBoxPvalueDouble.hide()

    def init_check_boxes(self):
        super().init_check_boxes()
        self.checkBoxAverage.hide()
        self.checkBoxStd.hide()
        self.checkBoxPvalueSingle.hide()
        self.checkBoxPvalueDouble.hide()

    def init_list(self):
        super().init_list()
        self.listWidget_2.hide()

    def get_item_string(self, item):
        return item.id

    def list_item_changed(self, index):
        enabled = True if index > -1 else False
        self.comboBoxSubject.setEnabled(enabled)
        self.update_visualization()

    def update_visualization(self):
        super().update_visualization()
        if self.listWidget.currentRow() == -1:
            return
        current_list_item = self.item_list[self.listWidget.currentRow()]
        values = current_list_item.data_dict['data'].value
        self.set_visualization(self.comboBoxSubject, values)

class GroupVisualizationWidget(VisualizationWidget):
    def __init_():
        super(VisualizationWidget, self).__init__(parent)

    def init_combo_boxes(self):
        super().init_combo_boxes()
        self.labelSubject.hide()
        self.comboBoxSubject.hide()
        self.comboBoxPvalueSingle.hide()
        self.comboBoxPvalueDouble.hide()

    def init_check_boxes(self):
        super().init_check_boxes()
        self.checkBoxPvalueSingle.hide()
        self.checkBoxPvalueDouble.hide()

    def init_list(self):
        super().init_list()
        self.listWidget_2.hide()

    def get_item_string(self, item):
        return item.name

    def list_item_changed(self, index):
        enabled = True if index > -1 else False
        self.checkBoxAverage.setEnabled(enabled)
        self.checkBoxStd.setEnabled(enabled)
        self.update_visualization()

    def update_visualization(self):
        super().update_visualization()
        if self.listWidget.currentRow() == -1:
            return
        current_list_item = self.item_list[self.listWidget.currentRow()]
        if self.checkBoxAverage.isChecked():
            values = current_list_item.averages()
            self.set_visualization(self.comboBoxAverage, values)
        if self.checkBoxStd.isChecked():
            values = current_list_item.standard_deviations()
            self.set_visualization(self.comboBoxStd, values)

class ComparisonVisualizationWidget(VisualizationWidget):
    def __init_():
        super(VisualizationWidget, self).__init__(parent)

    def init_combo_boxes(self):
        super().init_combo_boxes()
        self.labelSubject.hide()
        self.comboBoxSubject.hide()

    def get_item_string(self, item):
        return item.name

    def list_item_changed(self, index):
        enabled = True if index > -1 else False
        self.listWidget_2.setEnabled(enabled)
        self.update_visualization()

    def list_2_item_changed(self, index):
        enabled = True if index > -1 else False
        if enabled == False:
            self.checkBoxAverage.setEnabled(enabled)
            self.checkBoxStd.setEnabled(enabled)
            self.checkBoxPvalueSingle.setEnabled(enabled)
            self.checkBoxPvalueDouble.setEnabled(enabled)
        else:
            self.disable_check_boxes()
        self.update_visualization()

    def update_visualization(self):
        super().update_visualization()
        if self.listWidget.currentRow() == -1:
            return
        if self.listWidget_2.currentRow() == -1:
            return
        if self.listWidget.currentRow() == self.listWidget_2.currentRow():
            return
        current_list_item_1 = self.item_list[self.listWidget.currentRow()]
        current_list_item_2 = self.item_list[self.listWidget_2.currentRow()]
        averages, stds, p_values = current_list_item_1.comparison(current_list_item_2)
        if self.checkBoxAverage.isChecked():
            values = averages[0] - averages[1]
            self.set_visualization(self.comboBoxAverage, values)
        if self.checkBoxStd.isChecked():
            values = stds[0] - stds[1]
            self.set_visualization(self.comboBoxStd, values)
        if self.checkBoxPvalueSingle.isChecked():
            values = p_values[0]
            self.set_visualization(self.comboBoxPvalueSingle, values)
        if self.checkBoxPvalueDouble.isChecked():
            values = p_values[1]
            self.set_visualization(self.comboBoxPvalueDouble, values)


