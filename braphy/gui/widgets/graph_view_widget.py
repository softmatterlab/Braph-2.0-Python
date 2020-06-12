from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from pyqtgraph import ColorMap as cm
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative, QColor_to_list, QColor_from_list
from braphy.graph.graphs.graph import Graph
from braphy.workflows import *

ui_file = abs_path_from_relative(__file__, "../ui_files/graph_view_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class GraphViewWidget(Base, Form):
    def __init__(self, parent = None):
        super(GraphViewWidget, self).__init__(parent)
        self.setupUi(self)
        self.edge_color = QtGui.QColor('blue')
        self.init_buttons()
        self.init_check_boxes()
        self.init_spin_boxes()
        self.init_sliders()
        self.correlation = None
        self.btnColor.color = self.edge_color
        self.colormaps = self.get_colormaps()

    def init(self, brain_widget, analysis):
        self.brain_widget = brain_widget
        self.set_analysis(analysis)

    def set_analysis(self, analysis):
        self.analysis = analysis
        if analysis.__class__ == AnalysisMRI:
            self.comboBoxSubject.hide()
            self.btnGroup.hide()
            self.btnSubject.hide()
            self.btnGroup.setCheckable(False)
            self.btnSubject.setCheckable(False)
        self.init_combo_boxes()
        self.btnBinaryDensity.blockSignals(True)
        self.btnBinaryDensity.setChecked(True)
        self.btnBinaryDensity.blockSignals(False)
        self.spinBoxDensity.blockSignals(True)
        self.spinBoxDensity.setValue(0.2)
        self.spinBoxDensity.blockSignals(False)

    def init_buttons(self):
        self.btnGroup.clicked.connect(self.group)
        self.btnSubject.clicked.connect(self.subject)
        self.btnColor.clicked.connect(self.set_edge_color)
        self.btnWeighted.toggled.connect(self.weighted)
        self.btnBinaryDensity.toggled.connect(self.binary_density)
        self.btnBinaryThreshold.toggled.connect(self.binary_threshold)

        style_sheet = 'background-color: {};'.format(self.edge_color.name())
        self.btnColor.setStyleSheet(style_sheet)

    def init_combo_boxes(self):
        for group in self.analysis.cohort.groups:
            self.comboBoxGroup.addItem(group.name)
        #self.comboBoxGroup.setCurrentIndex(0)
        self.comboBoxGroup.currentIndexChanged.connect(self.update_correlation)
        self.comboBoxSubject.currentIndexChanged.connect(self.update_correlation)
        self.comboBoxColor.reset()
        for colormap in self.colormaps.values():
            self.comboBoxColor.add_colormap(colormap)
        self.comboBoxColor.setCurrentIndex(0)
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
        color = self.pick_color()
        if color.isValid():
            style_sheet = 'background-color: {};'.format(color.name())
            self.btnColor.setStyleSheet(style_sheet)
            self.btnColor.color = color
            self.brain_widget.set_brain_edge_color(QColor_to_list(color))

    def pick_color(self):
        options = QtWidgets.QColorDialog.ColorDialogOptions()
        options |= QtWidgets.QColorDialog.DontUseNativeDialog
        return QtWidgets.QColorDialog.getColor(options = options)

    def weighted(self, checked):
        if not checked:
            self.checkBoxColor.setChecked(False)
            self.checkBoxRadius.setChecked(False)
            return
        self.checkBoxColor.setEnabled(checked)
        self.checkBoxRadius.setEnabled(checked)
        self.update_visualization()

    def binary_density(self, checked):
        self.spinBoxDensity.setEnabled(checked)
        self.sliderDensity.setEnabled(checked)
        self.update_visualization()

    def binary_threshold(self, checked):
        self.spinBoxThreshold.setEnabled(checked)
        self.sliderThreshold.setEnabled(checked)
        self.update_visualization()

    def visualize_color(self, checked):
        self.comboBoxColor.setEnabled(checked)
        self.labelColor.setEnabled(not checked)
        self.btnColor.setEnabled(not checked)
        self.update_visualization()

    def visualize_radius(self, checked):
        self.labelMin.setEnabled(checked)
        self.spinBoxMin.setEnabled(checked)
        self.labelMax.setEnabled(checked)
        self.spinBoxMax.setEnabled(checked)
        self.labelRadius.setEnabled(not checked)
        self.spinBoxEdgeRadius.setEnabled(not checked)
        self.update_visualization()

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
        if self.btnGroup.isChecked():
            correlation = np.mean(correlation, axis = 0)
        elif self.btnSubject.isChecked():
            correlation = correlation[self.comboBoxSubject.currentIndex()]
        self.correlation = correlation
        self.update_visualization()

    def update_visualization(self):
        if self.correlation is None:
            self.update_correlation()
            return
        self.brain_widget.clear_gui_brain_edges()
        A = self.correlation
        A = Graph.remove_diagonal(A, np.mean(A))
        A = Graph.standardize(A, 'range')
        A = Graph.remove_diagonal(A, 0)
        edge_matrix = [[0]*A.shape[0]]*A.shape[0]
        default_radius = self.spinBoxEdgeRadius.value()
        default_color = self.btnColor.color
        if self.btnWeighted.isChecked():
            for (i, j), value in np.ndenumerate(A):
                if self.checkBoxColor.isChecked():
                    colormap = self.comboBoxColor.colormap()
                    color = colormap.map(value, mode = 'float')
                else:
                    color = default_color
                if self.checkBoxRadius.isChecked():
                    max_radius = self.spinBoxMax.value()
                    min_radius = self.spinBoxMin.value()
                    diff = max_radius - min_radius
                    radius = value * diff + min_radius
                else:
                    radius = default_radius
                edge_matrix[i][j] = (radius, color)
        else:
            if self.btnBinaryDensity.isChecked():
                A = self.analysis.correlation_density(A, self.spinBoxDensity.value())
            elif self.btnBinaryThreshold.isChecked():
                A = self.analysis.correlation_threshold(A, self.spinBoxThreshold.value())
            for (i, j), value in np.ndenumerate(A):
                edge_matrix[i][j] = (default_radius * value, default_color)
        edge_matrix = np.array(edge_matrix)
        self.brain_widget.set_edges(edge_matrix)

    def get_colormaps(self):
        colormaps = {}
        colormaps['spring'] = cm([0.0, 1.0], [[1.0, 0.28, 0.85, 1.0], [1.0, 0.94, 0.28, 1.0]])
        colormaps['cool'] = cm([0.0, 1.0], [[0.298, 0.964, 0.956, 1.0], [1.0, 0.28, 0.85, 1.0]])
        colormaps['hot'] = cm([0.0, 0.33, 0.67, 1.0], [[0.0, 0.0, 0.0, 1.0], [1.0, 0.0, 0.0, 1.0], [1.0, 1.0, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0]])
        colormaps['parula'] = cm([0.0, 0.5, 1.0], [[0.317, 0.223, 0.937, 1.0], [0.333, 0.666, 0.5, 1.0], [1.0, 0.94, 0.28, 1.0]])
        return colormaps









