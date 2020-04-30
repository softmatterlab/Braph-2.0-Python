from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative

ui_file = abs_path_from_relative(__file__, "../ui_files/correlation_matrix_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class CorrelationMatrixWidget(Base, Form):
    def __init__(self, parent = None):
        super(CorrelationMatrixWidget, self).__init__(parent)
        self.setupUi(self)

    def init(self):
        self.init_buttons()
        self.init_actions()
        self.radioButtonWeighted.setChecked(True)
        self.radioButtonGroup.setChecked(True)
        self.checkBoxDivide.setEnabled(False)
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
        self.actionZoom_in.triggered.connect(self.zoom_in)
        self.actionZoom_out.triggered.connect(self.zoom_out)
        self.actionPan_x_z.triggered.connect(self.pan_x_z)
        self.actionPan_x_y.triggered.connect(self.pan_x_y)
        self.actionInspect.triggered.connect(self.inspect)
        self.actionShow_labels.triggered.connect(self.show_labels)
        self.actionShow_colorbar.triggered.connect(self.show_colorbar)

        group = QtWidgets.QActionGroup(self)
        for action in (self.actionZoom_in, self.actionZoom_out, self.actionPan_x_z,
                       self.actionPan_x_y, self.actionInspect):
            group.addAction(action)

    def init_graphics_view(self):
        pass
        #self.correlationMatrix.init()

    def get_actions(self):
        actions = [self.actionZoom_in, self.actionZoom_out, self.actionPan_x_z, self.actionPan_x_y,
                   self.actionInspect, self.actionShow_labels, self.actionShow_colorbar]
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

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def pan_x_z(self):
        pass

    def pan_x_y(self):
        pass

    def inspect(self):
        pass

    def show_labels(self, state):
        self.correlationMatrix.show_labels(state)

    def show_colorbar(self, state):
        self.correlationMatrix.show_colorbar(state)


