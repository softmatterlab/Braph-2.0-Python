import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.utility.file_utility import abs_path_from_relative
from braphy.utility.math_utility import float_to_string
from braphy.utility.qt_utility import wait_cursor
import numpy as np
import time

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/calculation_window.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class CalculationData():
    def __init__(self, measures_dict, sub_measures, group_index, analysis, binary_values):
        self.measures_dict = measures_dict
        self.sub_measures = sub_measures
        self.group_index = group_index
        self.analysis = analysis
        self.binary_values = binary_values

class CalculationThread(QtCore.QThread):
    status = QtCore.pyqtSignal(str)

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.running = False
        self.calculation_data = None

    def calculate(self, calculation_data):
        self.calculation_data = calculation_data
        self.running = True

    def run(self):
        while True:
            if self.calculation_data is None or self.running == False:
                time.sleep(0.2)
                continue
            with wait_cursor():
                text_box_string = ' '
                self.status.emit(text_box_string)
                total_time = 0
                for sub_measure in self.calculation_data.sub_measures:
                    if not self.running:
                        break
                    start_time = time.time()
                    self.status.emit('Computing {}...\n'.format(sub_measure) + text_box_string)
                    measure_class = self.calculation_data.measures_dict[sub_measure]
                    if self.calculation_data.analysis.is_binary():
                        for value in self.calculation_data.binary_values:
                            if not self.running:
                                break
                            self.calculation_data.analysis.set_binary_value(value)
                            self.calculation_data.analysis.get_measurement(measure_class, sub_measure, self.calculation_data.group_index)
                    else:
                        self.calculation_data.analysis.get_measurement(measure_class, sub_measure, self.calculation_data.group_index)
                    duration = time.time() - start_time
                    total_time = total_time + duration
                    text_box_string = text_box_string + '\n{} {} s.'.format(sub_measure, float_to_string(duration, 3))
                    self.status.emit(text_box_string)
                text_box_string = 'DONE \nTotal time: {} s.\n'.format(float_to_string(total_time, 3)) + text_box_string
                self.status.emit(text_box_string)
                self.calculation_data = None

    def stop(self):
        self.calculation_data = None
        self.running = False

class CalculationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow, analysis, graph_type, update_callbacks = []):
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.analysis = analysis
        self.calculate_measures_window()
        self.graphMeasuresWidget.init(graph_type)

        self.init_buttons()
        self.init_combo_box()
        self.init_spin_boxes()

        self.update_callbacks = update_callbacks
        self.calculation_thread = CalculationThread()
        self.calculation_thread.status.connect(self.update_status_text)
        self.calculation_thread.start()

    def show_all_widgets(self):
        widgets = [self.comboBoxGroup2, self.labelPermutation, self.spinBoxPermutation, self.checkBoxLongitudinal,
                   self.labelBinary, self.labelMin, self.labelMax, self.labelStep, self.spinBoxMin, self.spinBoxMax, self.spinBoxStep, 
                   self.labelAttempts, self.labelWeights, self.labelRandomization, self.spinBoxAttempts, self.spinBoxWeights, self.spinBoxRandomization]
        for widget in widgets: 
            widget.show()

    def calculate_measures_window(self):
        self.show_all_widgets()
        self.comboBoxGroup2.hide()
        self.labelPermutation.hide()
        self.labelAttempts.hide()
        self.labelWeights.hide()
        self.labelRandomization.hide()
        self.spinBoxPermutation.hide()
        self.spinBoxAttempts.hide()
        self.spinBoxWeights.hide()
        self.spinBoxRandomization.hide()
        self.checkBoxLongitudinal.hide()
        self.setWindowTitle('Calculate group measures')
        self.btnCalculate.setText('Calculate group measures')

        if self.analysis.is_weighted():
            self.labelBinary.hide()
            self.labelMin.hide()
            self.labelMax.hide()
            self.labelStep.hide()
            self.spinBoxMin.hide()
            self.spinBoxMax.hide()
            self.spinBoxStep.hide()
        else:
            self.labelBinary.setText('Set {} values'.format(self.analysis.graph_settings.rule_binary))

    def compare_group_measures_window(self):
        self.show_all_widgets()
        self.btnCalculate.setText('Compare measures between groups')
        self.setWindowTitle('Compare measures between groups')

        self.labelAttempts.hide()
        self.labelWeights.hide()
        self.labelRandomization.hide()
        self.spinBoxAttempts.hide()
        self.spinBoxWeights.hide()
        self.spinBoxRandomization.hide()

        if self.analysis.is_weighted():
            self.labelBinary.hide()
            self.labelMin.hide()
            self.labelMax.hide()
            self.labelStep.hide()
            self.spinBoxMin.hide()
            self.spinBoxMax.hide()
            self.spinBoxStep.hide()
        else:
            self.labelBinary.setText('Set {} values'.format(self.analysis.graph_settings.rule_binary))

    def random_comparison_window(self):
        self.show_all_widgets()
        self.btnCalculate.setText('Compare measure with random group')
        self.setWindowTitle('Compare measure with random group')

        self.comboBoxGroup2.hide()
        self.labelPermutation.hide()
        self.spinBoxPermutation.hide()
        self.checkBoxLongitudinal.hide()

        if self.analysis.is_weighted():
            self.labelBinary.hide()
            self.labelMin.hide()
            self.labelMax.hide()
            self.labelStep.hide()
            self.spinBoxMin.hide()
            self.spinBoxMax.hide()
            self.spinBoxStep.hide()
        else:
            self.labelBinary.setText('Set {} values'.format(self.analysis.graph_settings.rule_binary))

    def init_buttons(self):
        self.btnCalculate.clicked.connect(self.calculation)
        self.btnMeasures.clicked.connect(self.calculate_measures_window)
        self.btnComparison.clicked.connect(self.compare_group_measures_window)
        self.btnRandomComparison.clicked.connect(self.random_comparison_window)        

    def init_combo_box(self):
        for group in self.analysis.cohort.groups:
            self.comboBoxGroup1.addItem(group.name)
            self.comboBoxGroup2.addItem(group.name)

    def init_spin_boxes(self):
        self.spinBoxMin.valueChanged.connect(self.min_changed)
        self.spinBoxMax.valueChanged.connect(self.max_changed)

    def calculation(self):
        if self.btnMeasures.isChecked():
            self.calculate_measures()
        elif self.btnComparison.isChecked():
            self.compare()
        elif self.btnRandomComparison.isChecked():
            self.compare_random()

    def calculate_measures(self):
        self.btnCalculate.setEnabled(False)
        measures_dict = self.graphMeasuresWidget.inverted_measures_dict
        sub_measures = self.graphMeasuresWidget.get_selected_measures()
        group_index = self.comboBoxGroup1.currentIndex()
        binary_values = np.arange(self.spinBoxMin.value(), self.spinBoxMax.value(), self.spinBoxStep.value())
        calculation_data = CalculationData(measures_dict, sub_measures, group_index,self.analysis,binary_values)
        self.calculation_thread.calculate(calculation_data)

    def compare(self):
        with wait_cursor():
            text_box_string = ' '
            self.textBrowser.setPlainText(text_box_string)
            QtGui.QApplication.processEvents()
            permutations = self.spinBoxPermutation.value()
            sub_measures = self.graphMeasuresWidget.get_selected_measures()
            group_index_1 = self.comboBoxGroup1.currentIndex()
            group_index_2 = self.comboBoxGroup2.currentIndex()
            longitudinal = self.checkBoxLongitudinal.isChecked()
            groups = (group_index_1, group_index_2)
            total_time = 0
            for sub_measure in sub_measures:
                start_time = time.time()
                self.textBrowser.setPlainText('Comparing {}...\n'.format(sub_measure) + text_box_string)
                QtGui.QApplication.processEvents()
                measure_class = self.graphMeasuresWidget.inverted_measures_dict[sub_measure]
                if self.analysis.is_binary():
                    binary_values = np.arange(self.spinBoxMin.value(), self.spinBoxMax.value(), self.spinBoxStep.value())
                    for value in binary_values:
                        self.analysis.set_binary_value(value)
                        self.analysis.get_comparison(measure_class, sub_measure, groups, permutations, longitudinal)
                else:
                    self.analysis.get_comparison(measure_class, sub_measure, groups, permutations, longitudinal)
                duration = time.time() - start_time
                total_time = total_time + duration
                text_box_string = text_box_string + '\n{} {} s.'.format(sub_measure, float_to_string(duration, 3))
                self.textBrowser.setPlainText(text_box_string)
                QtGui.QApplication.processEvents()
            text_box_string = 'DONE \nTotal time: {} s.\n'.format(float_to_string(total_time, 3)) + text_box_string
            self.textBrowser.setPlainText(text_box_string)
            QtGui.QApplication.processEvents()
        self.call_update()

    def compare_random(self):
        with wait_cursor():
            text_box_string = ' '
            self.textBrowser.setPlainText(text_box_string)
            QtGui.QApplication.processEvents()
            sub_measures = self.graphMeasuresWidget.get_selected_measures()
            group_index = self.comboBoxGroup1.currentIndex()
            attempts_per_edge = self.spinBoxAttempts.value()
            number_of_weights = self.spinBoxWeights.value()
            randomization_number = self.spinBoxRandomization.value()
            total_time = 0
            for sub_measure in sub_measures:
                start_time = time.time()
                self.textBrowser.setPlainText('Comparing {}...\n'.format(sub_measure) + text_box_string)
                QtGui.QApplication.processEvents()
                measure_class = self.graphMeasuresWidget.inverted_measures_dict[sub_measure]
                if self.analysis.is_binary():
                    binary_values = np.arange(self.spinBoxMin.value(), self.spinBoxMax.value(), self.spinBoxStep.value())
                    for value in binary_values:
                        self.analysis.set_binary_value(value)
                        self.analysis.get_random_comparison(measure_class, sub_measure, group_index,
                                                            attempts_per_edge, number_of_weights, randomization_number)
                else:
                    self.analysis.get_random_comparison(measure_class, sub_measure, group_index,
                                                        attempts_per_edge, number_of_weights, randomization_number)
                    pass
                duration = time.time() - start_time
                total_time = total_time + duration
                text_box_string = text_box_string + '\n{} {} s.'.format(sub_measure, float_to_string(duration, 3))
                self.textBrowser.setPlainText(text_box_string)
                QtGui.QApplication.processEvents()
            text_box_string = 'DONE \nTotal time: {} s.\n'.format(float_to_string(total_time, 3)) + text_box_string
            self.textBrowser.setPlainText(text_box_string)
            QtGui.QApplication.processEvents()
        self.call_update()

    def call_update(self):
        for func in self.update_callbacks:
            func()

    def min_changed(self, value):
        self.spinBoxMax.setMinimum(value)
        self.update_step()

    def max_changed(self, value):
        self.spinBoxMax.setMaximum(value)
        self.update_step()

    def update_step(self):
        self.spinBoxStep.setMaximum(self.spinBoxMax.value() - self.spinBoxMin.value())
    
    def update_status_text(self, msg):
        self.textBrowser.setPlainText(msg)
        if msg[:4] == 'DONE':
            self.call_update()
            self.btnCalculate.setEnabled(True)

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = CompareWithRandomGraph()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
