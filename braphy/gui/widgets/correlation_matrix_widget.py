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
        self.radioButtonWeighted.setChecked(True)
        self.radioButtonGroup.setChecked(True)
        self.checkBoxDivide.setEnabled(False)

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


