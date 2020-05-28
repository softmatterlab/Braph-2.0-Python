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
        self.radioButtonWeighted.setChecked(True)
        self.radioButtonGroup.setChecked(True)
        self.checkBoxDivide.setEnabled(False)

    def init(self, analysis, window):
        self.analysis = analysis
        self.init_comboboxes()
        self.init_graphics_view(window)

    def set_structural_view(self):
        self.radioButtonGroup.hide()
        self.radioButtonSubject.hide()
        self.comboBoxSubject.hide()

    def init_buttons(self):
        self.radioButtonGroup.toggled.connect(self.analyse_group)
        self.radioButtonSubject.toggled.connect(self.analyse_subject)
        self.radioButtonWeighted.toggled.connect(self.weighted_correlation)
        self.radioButtonHistogram.toggled.connect(self.histogram)
        self.radioButtonSubject.toggled.connect(self.analyse_subject)
        self.radioButtonDensity.toggled.connect(self.binary_correlation_density)
        self.radioButtonThreshold.toggled.connect(self.binary_correlation_threshold)

        self.checkBoxRearrange.stateChanged.connect(self.rearrange)
        self.checkBoxDivide.stateChanged.connect(self.divide)

    def init_actions(self):
        self.actionInspect.triggered.connect(self.inspect)
        self.actionShow_labels.triggered.connect(self.show_labels)
        self.actionShow_colorbar.triggered.connect(self.show_colorbar)

    def init_comboboxes(self):
        for group in self.analysis.cohort.groups:
            self.comboBoxGroup.addItem(group.name)
        for subject in self.analysis.cohort.subjects:
            self.comboBoxSubject.addItem(subject.id)
        self.comboBoxGroup.currentIndexChanged.connect(self.group_change)

    def init_sliders(self):
        self.spinboxThreshold.valueChanged.connect(self.set_threshold)
        self.horizontalSliderThreshold.valueChanged.connect(self.set_threshold)
        self.spinboxDensity.valueChanged.connect(self.set_density)
        self.horizontalSliderDensity.valueChanged.connect(self.set_density)

    def init_graphics_view(self, window):
        window.addToolBar(NavigationToolbar(self.correlationMatrix, self))
        self.group_change(0)

    def update_graphics_view(self):
        if self.correlation is None:
            return
        A = self.correlation
        if self.radioButtonDensity.isChecked():
            A = self.analysis.correlation_density(A, self.spinboxDensity.value())
        elif self.radioButtonThreshold.isChecked():
            A = self.analysis.correlation_threshold(A, self.spinboxThreshold.value())
        if self.checkBoxRearrange.isChecked():
            A = self.rearrange_regions(A)
        self.correlationMatrix.update_matrix(A)

    def group_change(self, idx):
        self.correlation = self.analysis.get_correlation(idx)
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
        sorted_regions = np.argsort(self.analysis.community_structure)
        new_A = A.copy()
        for (i, j), _ in np.ndenumerate(new_A):
            new_A[i, j] = A[sorted_regions[i], sorted_regions[j]]
        return new_A

    def analyse_group(self):
        self.comboBoxSubject.setEnabled(False)

    def analyse_subject(self):
        self.comboBoxSubject.setEnabled(True)

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


