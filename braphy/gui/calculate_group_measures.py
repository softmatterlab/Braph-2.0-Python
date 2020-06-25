import sys
import json
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.utility.helper_functions import abs_path_from_relative
import numpy as np

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/calculation_window.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CalculateGroupMeasures(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow, analysis, graph_type, update_callbacks = []):
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.comboBoxGroup2.hide()
        self.labelPermutation.hide()
        self.labelMatrix.hide()
        self.labelSwaps.hide()
        self.lineEditPermutation.hide()
        self.lineEditMatrix.hide()
        self.lineEditSwaps.hide()
        self.checkBoxLongitudinal.hide()
        if analysis.is_weighted():
            self.labelBinary.hide()
            self.labelMin.hide()
            self.labelMax.hide()
            self.labelStep.hide()
            self.spinBoxMin.hide()
            self.spinBoxMax.hide()
            self.spinBoxStep.hide()
        else:
            self.labelBinary.setText('Set {} values'.format(analysis.graph_settings.rule_binary))

        self.analysis = analysis
        self.graphMeasuresWidget.init(graph_type)

        self.init_buttons()
        self.init_combo_box()
        self.init_spin_boxes()

        self.update_callbacks = update_callbacks

    def init_buttons(self):
        self.btnCalculate.clicked.connect(self.calculate)
        self.btnResume.clicked.connect(self.resume)

    def init_combo_box(self):
        for group in self.analysis.cohort.groups:
            self.comboBoxGroup1.addItem(group.name)

    def init_spin_boxes(self):
        self.spinBoxMin.valueChanged.connect(self.min_changed)
        self.spinBoxMax.valueChanged.connect(self.max_changed)

    def calculate(self):
        sub_measures = self.graphMeasuresWidget.get_selected_measures()
        group_index = self.comboBoxGroup1.currentIndex()
        for sub_measure in sub_measures:
            measure_class = self.graphMeasuresWidget.inverted_measures_dict[sub_measure]
            if self.analysis.is_binary():
                binary_values = np.arange(self.spinBoxMin.value(), self.spinBoxMax.value(), self.spinBoxStep.value())
                for value in binary_values:
                    self.analysis.set_binary_value(value)
                    self.analysis.get_measurement(measure_class, sub_measure, group_index)
            else:
                self.analysis.get_measurement(measure_class, sub_measure, group_index)
        self.textBrowser.setPlainText('DONE')
        self.call_update()

    def call_update(self):
        for func in self.update_callbacks:
            func()

    def resume(self):
        pass

    def min_changed(self, value):
        self.spinBoxMax.setMinimum(value)
        self.update_step()

    def max_changed(self, value):
        self.spinBoxMax.setMaximum(value)
        self.update_step()

    def update_step(self):
        self.spinBoxStep.setMaximum(self.spinBoxMax.value() - self.spinBoxMin.value())

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = CalculateGroupMeasures()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
