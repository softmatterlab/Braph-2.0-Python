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
        self.init_buttons()
        self.init_actions()
        self.radioButtonWeighted.setChecked(True)
        self.radioButtonGroup.setChecked(True)
        self.checkBoxDivide.setEnabled(False)

    def init(self, analysis):
        self.analysis = analysis
        self.init_comboboxes()
        self.init_graphics_view()

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
        self.comboBoxGroup.currentIndexChanged.connect(self.update_graphics_view)

    def init_graphics_view(self):
        self.parent().parent().addToolBar(NavigationToolbar(self.correlationMatrix, self))
        self.update_graphics_view()

    def update_graphics_view(self):
        graph = self.analysis.get_graph(self.comboBoxGroup.currentIndex())
        self.correlationMatrix.init(graph.A)

    def get_actions(self):
        actions = [self.actionShow_labels, self.actionShow_colorbar, self.actionInspect]
        return actions

    def analyse_group(self):
        self.comboBoxSubject.setEnabled(False)

    def analyse_subject(self):
        self.comboBoxSubject.setEnabled(True)

    def weighted_correlation(self):
        self.textEditThreshold.setEnabled(False)
        self.horizontalSliderThreshold.setEnabled(False)
        self.textEditDensity.setEnabled(False)
        self.horizontalSliderDensity.setEnabled(False)

    def histogram(self):
        self.textEditThreshold.setEnabled(False)
        self.horizontalSliderThreshold.setEnabled(False)
        self.textEditDensity.setEnabled(False)
        self.horizontalSliderDensity.setEnabled(False)

    def binary_correlation_density(self):
        self.textEditDensity.setEnabled(True)
        self.horizontalSliderDensity.setEnabled(True)
        self.textEditThreshold.setEnabled(False)
        self.horizontalSliderThreshold.setEnabled(False)

    def binary_correlation_threshold(self):
        self.textEditThreshold.setEnabled(True)
        self.horizontalSliderThreshold.setEnabled(True)
        self.textEditDensity.setEnabled(False)
        self.horizontalSliderDensity.setEnabled(False)

    def rearrange(self):
        if self.checkBoxRearrange.isChecked():
            self.checkBoxDivide.setEnabled(True)
        else:
            self.checkBoxDivide.setEnabled(False)

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


