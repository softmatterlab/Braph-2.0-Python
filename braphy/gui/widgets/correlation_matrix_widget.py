from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.gui.widgets.correlation_matrix_visualizer import CorrelationMatrixVisualizer
from matplotlib.backends.backend_qt5agg import (
            NavigationToolbar2QT as NavigationToolbar)
from braphy.utility.helper_functions import abs_path_from_relative

ui_file = abs_path_from_relative(__file__, "../ui_files/correlation_matrix_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class CorrelationMatrixWidget(Base, Form):
    def __init__(self, parent = None):
        super(CorrelationMatrixWidget, self).__init__(parent)
        self.setupUi(self)
        self.correlation = None
        self.init_buttons()
        self.init_actions()
        self.init_sliders()
        self.btnWeighted.setChecked(True)
        self.btnGroup.setChecked(True)
        self.checkBoxDivide.setEnabled(False)

    def init(self, analysis, window):
        self.analysis = analysis
        self.init_comboboxes()
        self.init_graphics_view(window)

    def set_structural_view(self):
        self.btnGroup.hide()
        self.btnGroup.setCheckable(False)
        self.btnSubject.hide()
        self.comboBoxSubjects.hide()

    def init_buttons(self):
        self.btnGroup.toggled.connect(self.analyse_group)
        self.btnSubject.toggled.connect(self.analyse_subject)
        self.btnWeighted.toggled.connect(self.weighted_correlation)
        self.btnHistogram.toggled.connect(self.histogram)
        self.btnSubject.toggled.connect(self.analyse_subject)
        self.btnDensity.toggled.connect(self.binary_correlation_density)
        self.btnThreshold.toggled.connect(self.binary_correlation_threshold)

        self.checkBoxRearrange.stateChanged.connect(self.rearrange)
        self.checkBoxDivide.stateChanged.connect(self.divide)

    def init_actions(self):
        self.actionInspect.triggered.connect(self.inspect)
        self.actionShow_labels.triggered.connect(self.show_labels)
        self.actionShow_colorbar.triggered.connect(self.show_colorbar)

    def init_comboboxes(self):
        for group in self.analysis.cohort.groups:
            self.comboBoxGroup.addItem(group.name)
        self.comboBoxGroup.currentIndexChanged.connect(self.group_change)
        self.comboBoxSubjects.currentIndexChanged.connect(self.update_correlation)
        self.update_combo_box_subjects()

    def update_combo_box_subjects(self):
        self.comboBoxSubjects.clear()
        current_group_index = self.comboBoxGroup.currentIndex()
        if current_group_index == -1:
            return
        for subject in self.analysis.cohort.groups[current_group_index].subjects:
            self.comboBoxSubjects.addItem(subject.id)
        self.comboBoxSubjects.blockSignals(True)
        self.comboBoxSubjects.setCurrentIndex(0)
        self.comboBoxSubjects.blockSignals(False)

    def init_sliders(self):
        self.spinboxThreshold.valueChanged.connect(self.set_threshold)
        self.horizontalSliderThreshold.valueChanged.connect(self.set_threshold)
        self.spinboxDensity.valueChanged.connect(self.set_density)
        self.horizontalSliderDensity.valueChanged.connect(self.set_density)

    def init_graphics_view(self, window):
        window.addToolBar(NavigationToolbar(self.correlationMatrix, self))
        self.update_correlation()

    def update_graphics_view(self):
        if self.correlation is None:
            return
        A = self.correlation
        if self.btnDensity.isChecked():
            A = self.analysis.correlation_density(A, self.spinboxDensity.value())
        elif self.btnThreshold.isChecked():
            A = self.analysis.correlation_threshold(A, self.spinboxThreshold.value())
        if self.checkBoxRearrange.isChecked():
            A = self.rearrange_regions(A)
        self.correlationMatrix.update_matrix(A)

    def group_change(self):
        self.update_combo_box_subjects()
        self.update_correlation()

    def update_correlation(self):
        idx = self.comboBoxGroup.currentIndex()
        if idx == -1:
            return
        correlation = self.analysis.get_correlation(idx)
        if self.btnGroup.isChecked():
            correlation = np.mean(correlation, 0)
        elif self.btnSubject.isChecked():
            correlation = correlation[self.comboBoxSubjects.currentIndex()]
        self.correlation = correlation
        self.update_graphics_view()

    def get_actions(self):
        actions = [self.actionShow_labels, self.actionShow_colorbar, self.actionInspect]
        return actions

    def set_threshold(self, value):
        if not isinstance(value, float):
            value = value/100.0
        self.spinboxThreshold.setValue(value)
        self.horizontalSliderThreshold.setValue(int(value*100))
        self.update_graphics_view()

    def set_density(self, value):
        if not isinstance(value, float):
            value = value/100.0
        self.spinboxDensity.setValue(value)
        self.horizontalSliderDensity.setValue(int(value*100))
        self.update_graphics_view()

    def rearrange_regions(self, A):
        group_index = self.comboBoxGroup.currentIndex()
        sorted_regions = np.argsort(self.analysis.community_structure[group_index])
        new_A = A.copy()
        for (i, j), _ in np.ndenumerate(new_A):
            new_A[i, j] = A[sorted_regions[i], sorted_regions[j]]
        return new_A

    def analyse_group(self):
        self.comboBoxSubjects.setEnabled(False)
        self.update_correlation()

    def analyse_subject(self):
        self.comboBoxSubjects.setEnabled(True)
        self.update_correlation()

    def weighted_correlation(self):
        self.spinboxThreshold.setEnabled(False)
        self.horizontalSliderThreshold.setEnabled(False)
        self.spinboxDensity.setEnabled(False)
        self.horizontalSliderDensity.setEnabled(False)
        self.update_graphics_view()

    def histogram(self):
        self.spinboxThreshold.setEnabled(False)
        self.horizontalSliderThreshold.setEnabled(False)
        self.spinboxDensity.setEnabled(False)
        self.horizontalSliderDensity.setEnabled(False)

    def binary_correlation_density(self):
        self.spinboxDensity.setEnabled(True)
        self.horizontalSliderDensity.setEnabled(True)
        self.spinboxThreshold.setEnabled(False)
        self.horizontalSliderThreshold.setEnabled(False)
        self.update_graphics_view()

    def binary_correlation_threshold(self):
        self.spinboxThreshold.setEnabled(True)
        self.horizontalSliderThreshold.setEnabled(True)
        self.spinboxDensity.setEnabled(False)
        self.horizontalSliderDensity.setEnabled(False)
        self.update_graphics_view()

    def rearrange(self, state):
        self.checkBoxDivide.setEnabled(state)
        self.update_graphics_view()

    def divide(self):
        pass

    def set_cursor(self, file_name):
        cursor_file = abs_path_from_relative(__file__, file_name)
        pm = QtGui.QPixmap(cursor_file)
        cursor = QtGui.QCursor(pm)
        self.setCursor(cursor)

    def inspect(self, checked):
        if checked:
            self.set_cursor('../icons/cursor.png')
        else:
            self.unsetCursor()
            self.correlationMatrix.clear_text()
            self.correlationMatrix.draw()
        self.correlationMatrix.mouse_mode_inspect = checked

    def show_labels(self, state):
        self.correlationMatrix.show_labels(state)

    def show_colorbar(self, state):
        self.correlationMatrix.show_colorbar(state)


