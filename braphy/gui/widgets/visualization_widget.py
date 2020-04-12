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

    def init(self, visualize_groups, brain_widget, settings_widget):
        self.visualize_groups = visualize_groups
        self.init_combo_boxes()
        self.init_check_boxes()
        self.init_list([])
        self.brain_widget = brain_widget
        self.settings_widget = settings_widget

    def init_combo_boxes(self):
        for option in self.visualization_options:
            self.comboBoxAverage.addItem(option)
            self.comboBoxStd.addItem(option)
            self.comboBoxSubject.addItem(option)
        self.comboBoxAverage.setCurrentIndex(-1)
        self.comboBoxStd.setCurrentIndex(-1)
        self.comboBoxSubject.setCurrentIndex(-1)

        if self.visualize_groups:
            self.labelSubject.hide()
            self.comboBoxSubject.hide()
        else:
            self.checkBoxAverage.hide()
            self.checkBoxStd.hide()
            self.comboBoxAverage.hide()
            self.comboBoxStd.hide()

        for colormap in self.colormaps.values():
            self.comboBoxColormap.add_colormap(colormap)

        self.comboBoxAverage.currentIndexChanged.connect(self.set_average_visualization)
        self.comboBoxStd.currentIndexChanged.connect(self.set_std_visualization)
        self.comboBoxSubject.currentIndexChanged.connect(self.update_visualization)
        self.comboBoxColormap.currentIndexChanged.connect(self.update_visualization)

        self.comboBoxAverage.setEnabled(False)
        self.comboBoxStd.setEnabled(False)
        self.comboBoxSubject.setEnabled(False)

    def init_check_boxes(self):
        self.checkBoxAverage.stateChanged.connect(self.visualize_average)
        self.checkBoxStd.stateChanged.connect(self.visualize_std)
        self.checkBoxAverage.setEnabled(False)
        self.checkBoxStd.setEnabled(False)

    def init_list(self, item_list):
        self.item_list = item_list
        self.listWidget.blockSignals(True)
        self.listWidget.clear()
        self.listWidget.currentRowChanged.connect(self.list_item_changed)
        for item in item_list:
            if self.visualize_groups:
                self.listWidget.addItem(item.name)
            else:
                self.listWidget.addItem(item.id)
        self.listWidget.blockSignals(False)

    def list_item_changed(self, index):
        items = [self.checkBoxAverage, self.checkBoxStd, self.comboBoxSubject]
        enabled = True if index > -1 else False
        for item in items:
            item.setEnabled(enabled)

    def set_average_visualization(self, index): # combo box
        if self.comboBoxStd.currentIndex() == index:
            self.comboBoxStd.blockSignals(True)
            self.comboBoxStd.setCurrentIndex(-1)
            self.comboBoxStd.blockSignals(False)
        self.update_visualization()

    def set_std_visualization(self, index): # combo box
        if self.comboBoxAverage.currentIndex() == index:
            self.comboBoxAverage.blockSignals(True)
            self.comboBoxAverage.setCurrentIndex(-1)
            self.comboBoxAverage.blockSignals(False)
        self.update_visualization()

    def visualize_average(self, state): # check box
        self.comboBoxAverage.setEnabled(state)
        self.update_visualization()

    def visualize_std(self, state): # check box
        self.comboBoxStd.setEnabled(state)
        self.update_visualization()

    def update_visualization(self):
        self.settings_widget.init_brain_region_color()
        self.settings_widget.change_brain_region_size()

        current_list_item = self.item_list[self.listWidget.currentRow()]
        if self.visualize_groups:
            if self.checkBoxAverage.isChecked():
                values = current_list_item.averages()
                self.set_visualization(self.comboBoxAverage, values)
            if self.checkBoxStd.isChecked():
                values = current_group.standard_deviations()
                self.set_visualization(self.comboBoxStd, values)
        else:
            values = current_list_item.data_dict['data'].value
            self.set_visualization(self.comboBoxSubject, values)

    def set_visualization(self, combo_box, values):
        values_min = np.min(values)
        values_max = np.max(values)
        values = (values - values_min)/(values_max - values_min)
        visualization_type = combo_box.currentText()
        for i, region in enumerate(self.brain_widget.gui_brain_regions):
            if visualization_type == 'Color':
                region.set_color(self.get_color(values[i]))
            if visualization_type == 'Size':
                region.set_size(values[i] * 7 + 1)

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

