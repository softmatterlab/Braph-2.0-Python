from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from pyqtgraph import ColorMap as cm
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.workflows import *

ui_file = abs_path_from_relative(__file__, "../ui_files/graph_view_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class GraphViewWidget(Base, Form):
    def __init__(self, parent = None):
        super(GraphViewWidget, self).__init__(parent)
        self.setupUi(self)
        self.init_buttons()
        self.init_check_boxes()
        self.init_spin_boxes()
        self.init_sliders()

    def init(self, brain_widget):
        self.brain_widget = brain_widget

    def set_analysis(self, analysis):
        self.analysis = analysis
        if analysis.__class__ == AnalysisMRI:
            self.comboBoxSubject.hide()
            self.btnGroup.hide()
            self.btnSubject.hide()
        self.init_combo_boxes()

    def init_buttons(self):
        self.btnGroup.clicked.connect(self.group)
        self.btnSubject.clicked.connect(self.subject)
        self.btnColor.clicked.connect(self.set_edge_color)
        self.btnWeighted.toggled.connect(self.weighted)
        self.btnBinaryDensity.toggled.connect(self.binary_density)
        self.btnBinaryThreshold.toggled.connect(self.binary_threshold)

    def init_combo_boxes(self):
        for group in self.analysis.cohort.groups:
            self.comboBoxGroup.addItem(group.name)
        self.comboBoxGroup.currentIndexChanged.connect(self.update_correlation)
        self.comboBoxGroup.setCurrentIndex(0)
        self.comboBoxSubject.currentIndexChanged.connect(self.update_correlation)
        self.comboBoxColor.currentIndexChanged.connect(self.update_visualization)

    def init_check_boxes(self):
        self.checkBoxColor.stateChanged.connect(self.visualize_color)
        self.checkBoxRadius.stateChanged.connect(self.visualize_radius)

    def init_spin_boxes(self):
        self.spinBoxEdgeRadius.valueChanged.connect(self.update_visualization)
        self.spinBoxMin.valueChanged.connect(self.update_visualization)
        self.spinBoxMax.valueChanged.connect(self.update_visualization)
        self.spinBoxDensity.valueChanged.connect(self.set_density)
        self.spinBoxThreshold.valueChanged.connect(self.set_threshold)

    def init_sliders(self):
        self.sliderDensity.valueChanged.connect(self.set_density)
        self.sliderThreshold.valueChanged.connect(self.set_threshold)

    def group(self, checked):
        if checked:
            self.comboBoxSubject.setEnabled(False)

    def subject(self, checked):
        if checked:
            self.comboBoxSubject.setEnabled(True)
            self.update_subject_combo_box()

    def update_subject_combo_box(self):
        self.comboBoxSubject.blockSignals(True)
        self.comboBoxSubject.clear()
        group_index = self.comboBoxGroup.currentIndex()
        for subject in self.analysis.cohort.groups[group_index].subjects:
            self.comboBoxSubject.addItem(subject.id)
        self.comboBoxSubject.blockSignals(False)

    def set_edge_color(self):
        pass

    def weighted(self, checked):
        if not checked:
            self.checkBoxColor.setChecked(False)
            self.checkBoxRadius.setChecked(False)
        self.checkBoxColor.setEnabled(checked)
        self.checkBoxRadius.setEnabled(checked)

    def binary_density(self, checked):
        self.spinBoxDensity.setEnabled(checked)
        self.sliderDensity.setEnabled(checked)

    def binary_threshold(self, checked):
        self.spinBoxThreshold.setEnabled(checked)
        self.sliderThreshold.setEnabled(checked)

    def visualize_color(self, checked):
        self.comboBoxColor.setEnabled(checked)
        self.labelColor.setEnabled(not checked)
        self.btnColor.setEnabled(not checked)

    def visualize_radius(self, checked):
        self.labelMin.setEnabled(checked)
        self.spinBoxMin.setEnabled(checked)
        self.labelMax.setEnabled(checked)
        self.spinBoxMax.setEnabled(checked)
        self.labelRadius.setEnabled(not checked)
        self.spinBoxEdgeRadius.setEnabled(not checked)

    def set_threshold(self, value):
        if not isinstance(value, float):
            value = value/100.0
        self.spinBoxThreshold.setValue(value)
        self.sliderThreshold.setValue(int(value*100))
        self.update_visualization()

    def set_density(self, value):
        if not isinstance(value, float):
            value = value/100.0
        self.spinBoxDensity.setValue(value)
        self.sliderDensity.setValue(int(value*100))
        self.update_visualization()

    def update_correlation(self):
        group_index = self.comboBoxGroup.currentIndex()
        if group_index == -1:
            return
        correlation = self.analysis.get_correlation(group_index)
        if btnGroup.is_checked():
            correlation = np.mean(correlation, axis = 0)
        elif btnSubject.isChecked():
            correlation = correlation[self.comboBoxSubject.currentIndex()]
        self.correlation = correlation
        self.update_visualization()

    def update_visualization(self):
        if self.correlation is None:
            return
        self.brainWidget.clear_edges()
        A = self.correlation
        if self.btnWeighted.isChecked():
            pass
        elif self.btnBinaryDensity.isChecked():
            A = self.analysis.correlation_density(A, self.spinBoxDensity.value())
        elif self.btnBinaryThreshold.isChecked():
            A = self.analysis.correlation_threshold(A, self.spinBoxThreshold.value())
        #build matrix
        #brainWidget.set_edges(matrix)








