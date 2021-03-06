from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
import pandas as pd
from braphy.utility.file_utility import abs_path_from_relative
from braphy.utility.qt_utility import FloatDelegate
from braphy.utility.math_utility import float_to_string, float_to_string_fix_decimals
from braphy.graph.measures.measure import Measure
import sys

ui_file = abs_path_from_relative(__file__, "../ui_files/measures_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class MeasuresWidget(Base, Form):
    def __init__(self, parent = None):
        super(MeasuresWidget, self).__init__(parent)
        self.setupUi(self)
        self.init_buttons()
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.tableWidget.itemSelectionChanged.connect(self.enable_add_plot)
        self.btnAdd.setEnabled(False)

    def init(self, measure_type, analysis, update_functions = None):
        self.analysis = analysis
        self.measure_type = measure_type
        if measure_type == Measure.GLOBAL:
            self.comboBoxRegion.hide()
            self.comboBoxRegion2.hide()
            self.labelRegion.hide()
            self.binaryPlotWidget.tabWidget.tabBar().hide()
        elif measure_type == Measure.NODAL:
            self.comboBoxRegion2.hide()
            self.binaryPlotWidget.set_nodal()
        if analysis.cohort.subject_class.structural():
            self.btnGroup.hide()
            self.btnSubject.hide()
            self.comboBoxSubject.hide()
        if analysis.graph_settings.weighted:
            self.binaryPlotWidget.hide()
            self.btnAdd.hide()
        else:
            self.binaryPlotWidget.init(self.analysis)
        self.init_combo_boxes()
        self.btnMeasure.setChecked(True)
        self.measure()
        self.update_functions = update_functions

    def init_buttons(self):
        self.btnSelectAll.clicked.connect(self.tableWidget.selectAll)
        self.btnClearSelection.clicked.connect(self.tableWidget.clearSelection)
        self.btnRemove.clicked.connect(self.remove)

        self.btnMeasure.clicked.connect(self.measure)
        self.btnComparison.clicked.connect(self.comparison)
        self.btnRandomComparison.clicked.connect(self.random_comparison)

        self.btnGroup.clicked.connect(self.group_average)
        self.btnSubject.clicked.connect(self.subject)

        self.btnGroup.setChecked(True)

        self.btnAdd.clicked.connect(self.add_plot)
        self.btnExportTxt.clicked.connect(lambda state, file_type = 'txt', export_function = self.export_txt: self.export(file_type, export_function))
        self.btnExportXlsx.clicked.connect(lambda state, file_type = 'xlsx', export_function = self.export_xlsx: self.export(file_type, export_function))

    def init_combo_boxes(self):
        self.comboBoxRegion.currentIndexChanged.connect(self.update_table)
        self.comboBoxRegion2.currentIndexChanged.connect(self.update_table)
        self.comboBoxGroup1.currentIndexChanged.connect(self.group_changed)
        self.comboBoxGroup2.currentIndexChanged.connect(self.update_table)
        self.comboBoxSubject.currentIndexChanged.connect(self.update_table)

        for group in self.analysis.cohort.groups:
            self.comboBoxGroup1.addItem(group.name)
            self.comboBoxGroup2.addItem(group.name)

        for label in self.analysis.cohort.atlas.get_brain_region_labels():
            self.comboBoxRegion.addItem(label)
            self.comboBoxRegion2.addItem(label)

    def run_update_functions(self):
        for function in self.update_functions:
            function()

    def add_matrix_plot(self):
        selected = self.get_selected()[0]
        binary_values = []
        node_values = []
        current_group_1 = self.comboBoxGroup1.currentIndex()
        current_group_2 = self.comboBoxGroup2.currentIndex()
        if self.is_measure():
            index = self.measurement_index_mapping[selected]
            sub_measure = self.analysis.measurements[index].sub_measure
            for measurement in self.analysis.measurements:
                if (measurement.sub_measure == sub_measure and
                    measurement.group == current_group_1):
                    if self.analysis.functional():
                        if self.btnGroup.isChecked():
                            value = np.mean(measurement.value, axis = 0)
                        else:
                            value = measurement.value[self.comboBoxSubject.currentIndex()]
                    else:
                        value = (measurement.value)
                    node_values.append(value)
                    binary_values.append(measurement.binary_value)

        if self.is_comparison():
            index = self.comparison_index_mapping[selected]
            sub_measure = self.analysis.comparisons[index].sub_measure
            for comparison in self.analysis.comparisons:
                if (comparison.sub_measure == sub_measure and
                    comparison.groups[0] == current_group_1 and
                    comparison.groups[1] == current_group_2):
                    if self.analysis.functional():
                        value_1 = np.mean(comparison.measures[0], axis = 0)
                        value_2 = np.mean(comparison.measures[1], axis = 0)
                    else:
                        value_1 = comparison.measures[0]
                        value_2 = comparison.measures[1]
                    node_values.append(value_2 - value_1)
                    binary_values.append(comparison.binary_value)

        if self.is_random_comparison():
            index = self.random_comparison_index_mapping[selected]
            sub_measure = self.analysis.random_comparisons[index].sub_measure
            for random_comparison in self.analysis.random_comparisons:
                if (random_comparison.sub_measure == sub_measure and
                    random_comparison.group_index == current_group_1):
                    binary_values.append(random_comparison.binary_value)
                    node_values.append(random_comparison.difference)
        
        binary_values = np.array(binary_values)
        node_values = np.array(node_values)
        sorted_indices = np.argsort(binary_values)
        node_values = node_values[sorted_indices,:]
        binary_values = np.sort(binary_values)
        title = sub_measure
        if len(node_values.shape) > 2:
            self.binaryPlotWidget.matrix = node_values
            node_values = node_values[:, 0, :]
            title = title + ', {}'.format(self.analysis.cohort.atlas.get_brain_region_labels()[0])
        self.binaryPlotWidget.binaryMatrixPlotVisualizer.plot(node_values, title, binary_values)

    def add_plot(self):
        if self.binaryPlotWidget.tab_index() == 1:
            self.add_matrix_plot()
            return
        selected = self.get_selected()
        info_strings = {}
        all_values = {}
        confidence_intervals = None
        sub_measures = []
        for i in selected:
            sub_measure = None
            if self.is_measure():
                index = self.measurement_index_mapping[i]
                sub_measure = self.analysis.measurements[index].sub_measure

            elif self.is_comparison():
                index = self.comparison_index_mapping[i]
                sub_measure = self.analysis.comparisons[index].sub_measure
                group_2 = self.comboBoxGroup2.currentIndex()
                confidence_intervals = {}

            elif self.is_random_comparison():
                index = self.random_comparison_index_mapping[i]
                sub_measure = self.analysis.random_comparisons[index].sub_measure
                confidence_intervals = {}

            if sub_measure and sub_measure not in sub_measures:
                sub_measures.append(sub_measure)

        if self.is_measure():
            headers = self.measurement_labels()
            value_column = headers.index('Value')
        elif self.is_comparison():
            headers = self.comparison_labels()
            value_column = headers.index('Difference')
            CI_lower_column = headers.index('CI lower')
            CI_upper_column = headers.index('CI upper')
        elif self.is_random_comparison():
            headers = self.random_comparison_labels()
            value_column = headers.index('Difference')
            CI_lower_column = headers.index('CI lower')
            CI_upper_column = headers.index('CI upper')
        measure_column = headers.index('Measure')
        binary_column = headers.index(self.analysis.graph_settings.rule_binary)

        for row in range(self.tableWidget.rowCount()):
            sub_measure = self.tableWidget.item(row, measure_column).text()
            if sub_measure in sub_measures:
                binary_value = float(self.tableWidget.item(row, binary_column).text())
                value = float(self.tableWidget.item(row, value_column).text())
                if sub_measure not in all_values.keys():
                    all_values[sub_measure] = []
                    info_string = self.get_info_string(sub_measure)
                    info_strings[sub_measure] = info_string
                all_values[sub_measure].append([binary_value, value])
                if confidence_intervals is not None:
                    CI_lower = float(self.tableWidget.item(row, CI_lower_column).text())
                    CI_upper = float(self.tableWidget.item(row, CI_upper_column).text())
                    if sub_measure not in confidence_intervals.keys():
                        confidence_intervals[sub_measure] = [[],[]]
                    confidence_intervals[sub_measure][0].append(CI_lower)
                    confidence_intervals[sub_measure][1].append(CI_upper)

        for sub_measure, values in all_values.items():
            ci = None if confidence_intervals is None else np.array(confidence_intervals[sub_measure])
            self.binaryPlotWidget.add_plot(info_strings[sub_measure], np.array(values), ci)

    def enable_add_plot(self):
        selected = self.get_selected()
        self.btnAdd.setEnabled(len(selected)>0)

    def get_info_string(self, sub_measure):
        info_string = []
        if self.is_measure():
            info_string.append('Measure')
        elif self.is_comparison():
            info_string.append('Comparison')
        elif self.is_random_comparison():
            info_string.append('Random comparison')
        group_1 = self.analysis.cohort.groups[self.comboBoxGroup1.currentIndex()].name
        group_2 = self.analysis.cohort.groups[self.comboBoxGroup2.currentIndex()].name
        subject = self.analysis.cohort.subjects[self.comboBoxSubject.currentIndex()].id
        region_1 = self.comboBoxRegion.currentText()
        region_2 = self.comboBoxRegion2.currentText()
        info_string.extend([sub_measure, group_1, group_2, subject, region_1, region_2])
        is_subject = self.analysis.cohort.subject_class.functional() and not self.btnGroup.isChecked()
        mask = [True, True, True, self.comboBoxGroup2.isEnabled(), is_subject, self.measure_type != Measure.GLOBAL, self.measure_type == Measure.BINODAL]
        info_string = np.array(info_string)[np.where(mask)[0]].tolist()
        info_string = ' - '.join(info_string)
        return info_string

    def remove(self):
        selected = self.get_selected()
        for i in range(len(selected) - 1, -1, -1):
            if self.is_measure():
                index_to_remove = self.measurement_index_mapping[selected[i]]
                del self.analysis.measurements[index_to_remove]
            elif self.is_comparison():
                index_to_remove = self.comparison_index_mapping[selected[i]]
                del self.analysis.comparisons[index_to_remove]
            elif self.is_random_comparison():
                index_to_remove = self.random_comparison_index_mapping[selected[i]]
                del self.analysis.random_comparisons[index_to_remove]
        if self.measure_type == Measure.NODAL:
            self.run_update_functions()
        self.update_table()

    def measure(self):
        self.comboBoxGroup2.setEnabled(False)
        if not self.btnGroup.isChecked():
            self.comboBoxSubject.setEnabled(True)
        self.btnSubject.setEnabled(True)
        self.labelGroup.setText('Choose group:')
        self.update_table()

    def is_measure(self):
        return self.btnMeasure.isChecked()

    def comparison(self):
        self.comboBoxGroup2.setEnabled(True)
        self.comboBoxSubject.setEnabled(False)
        self.btnSubject.setEnabled(False)
        self.labelGroup.setText('Choose groups:')
        self.btnGroup.blockSignals(True)
        self.btnGroup.setChecked(True)
        self.btnGroup.blockSignals(False)
        self.update_table()

    def is_comparison(self):
        return self.btnComparison.isChecked()

    def random_comparison(self):
        self.comboBoxGroup2.setEnabled(False)
        self.comboBoxSubject.setEnabled(False)
        self.btnSubject.setEnabled(False)
        self.labelGroup.setText('Choose group:')
        self.btnGroup.blockSignals(True)
        self.btnGroup.setChecked(True)
        self.btnGroup.blockSignals(False)
        self.update_table()

    def is_random_comparison(self):
        return self.btnRandomComparison.isChecked()

    def group_changed(self):
        if self.btnSubject.isChecked():
            self.subject()
        self.update_table()

    def group_average(self):
        self.comboBoxSubject.setEnabled(False)
        self.update_table()

    def subject(self):
        self.comboBoxSubject.blockSignals(True)
        self.comboBoxSubject.setEnabled(True)
        self.comboBoxSubject.clear()
        group = self.analysis.cohort.groups[self.comboBoxGroup1.currentIndex()]
        for subject in group.subjects:
            self.comboBoxSubject.addItem(subject.id)
        self.comboBoxSubject.blockSignals(False)
        self.update_table()

    def update_table(self):
        self.tableWidget.clear_table()
        current_group_1 = self.comboBoxGroup1.currentIndex()
        current_group_2 = self.comboBoxGroup2.currentIndex()
        current_region_index = self.comboBoxRegion.currentIndex()
        if self.is_measure():
            self.update_measurements_table(current_group_1, current_region_index)
        elif self.is_comparison():
            self.update_comparison_table(current_group_1, current_group_2, current_region_index)
        elif self.is_random_comparison():
            self.update_random_comparison_table(current_group_1, current_region_index)

    def update_measurements_table(self, current_group, current_region_index):
        labels = self.measurement_labels()
        self.tableWidget.setColumnCount(len(labels))
        self.tableWidget.setHorizontalHeaderLabels(labels)
        self.measurement_index_mapping = {}
        for i, measurement in enumerate(self.analysis.measurements):
            if measurement.dimension() == self.measure_type and current_group == measurement.group:
                row = self.tableWidget.rowCount()
                self.measurement_index_mapping[row] = i
                self.tableWidget.setRowCount(row + 1)
                contents = self.measurement_contents(measurement)
                for j, content in enumerate(contents):
                    item = QTableWidgetItem(content)
                    item.setFlags(self.table_flags)
                    self.tableWidget.setItem(row, j, item)

    def update_comparison_table(self, current_group_1, current_group_2, current_region_index):
        labels = self.comparison_labels()
        self.tableWidget.setColumnCount(len(labels))
        self.tableWidget.setHorizontalHeaderLabels(labels)
        self.comparison_index_mapping = {}
        for i, comparison in enumerate(self.analysis.comparisons):
            if comparison.dimension() == self.measure_type and current_group_1 == comparison.groups[0] and current_group_2 == comparison.groups[1]:
                row = self.tableWidget.rowCount()
                self.comparison_index_mapping[row] = i
                self.tableWidget.setRowCount(row + 1)
                contents = self.comparison_contents(comparison)
                for j, content in enumerate(contents):
                    item = QTableWidgetItem(content)
                    item.setFlags(self.table_flags)
                    self.tableWidget.setItem(row, j, item)

    def update_random_comparison_table(self, current_group, current_region_index):
        labels = self.random_comparison_labels()
        self.tableWidget.setColumnCount(len(labels))
        self.tableWidget.setHorizontalHeaderLabels(labels)
        self.random_comparison_index_mapping = {}
        for i, random_comparison in enumerate(self.analysis.random_comparisons):
            if random_comparison.dimension() == self.measure_type and current_group == random_comparison.group_index:
                row = self.tableWidget.rowCount()
                self.random_comparison_index_mapping[row] = i
                self.tableWidget.setRowCount(row + 1)
                contents = self.random_comparison_contents(random_comparison)
                for j, content in enumerate(contents):
                    item = QTableWidgetItem(content)
                    item.setFlags(self.table_flags)
                    self.tableWidget.setItem(row, j, item)

    def measurement_mask(self):
        subject = self.analysis.functional() and not self.btnGroup.isChecked()
        binary = self.analysis.is_binary()
        nodal = self.measure_type == Measure.NODAL
        binodal = self.measure_type == Measure.BINODAL
        mask = [True, subject, True, True, binary, nodal, binodal, binodal, True, True]

        return mask

    def measurement_labels(self):
        rule_binary = self.analysis.graph_settings.rule_binary
        labels = ['Group', 'Subject', 'Measure', 'Param', rule_binary, 'Region', 'Region 1', 'Region 2', 'Value', 'Notes']

        mask = self.measurement_mask()
        labels = np.array(labels)[np.where(mask)[0]].tolist()
        return labels

    def measurement_contents(self, measurement):
        if self.analysis.functional():
            if self.btnGroup.isChecked():
                value = np.mean(measurement.value, axis = 0)
            else:
                value = measurement.value[self.comboBoxSubject.currentIndex()]
        else:
            value = (measurement.value)

        region_1_index = self.comboBoxRegion.currentIndex()
        region_2_index = self.comboBoxRegion2.currentIndex()

        group = self.analysis.cohort.groups[measurement.group].name
        subject = self.comboBoxSubject.currentText()
        measure = measurement.sub_measure
        param = '-'
        binary_value = float_to_string_fix_decimals(measurement.binary_value)
        region = self.comboBoxRegion.currentText()
        region_2 = self.comboBoxRegion2.currentText()
        if self.measure_type == Measure.BINODAL:
            value = value[region_1_index][region_2_index]
        elif self.measure_type == Measure.NODAL:
            value = value[region_1_index]
        value = float_to_string(value)
        notes = '-'
        content = [group, subject, measure, param, binary_value, region, region, region_2, value, notes]

        mask = self.measurement_mask()
        content = np.array(content)[np.where(mask)[0]].tolist()
        return content

    def comparison_mask(self):
        binary = self.analysis.is_binary()
        nodal = self.measure_type == Measure.NODAL
        binodal = self.measure_type == Measure.BINODAL
        mask = [True, True, True, True, binary, nodal, binodal, binodal] + [True]*8

        return mask

    def comparison_labels(self):
        rule_binary = self.analysis.graph_settings.rule_binary
        labels = ['Group 1', 'Group 2', 'Measure', 'Param', rule_binary, 'Region', 'Region 1', 'Region 2',
                  'Longitudinal', 'p (1-tailed)', 'p (2-tailed)', 'CI lower', 'CI upper', 'Value 1', 'Value 2', 'Difference']

        mask = self.comparison_mask()
        labels = np.array(labels)[np.where(mask)[0]].tolist()
        return labels

    def comparison_contents(self, comparison):
        if self.analysis.functional():
            value_1 = np.mean(comparison.measures[0], axis = 0)
            value_2 = np.mean(comparison.measures[1], axis = 0)
        else:
            value_1 = comparison.measures[0]
            value_2 = comparison.measures[1]

        region_1_index = self.comboBoxRegion.currentIndex()
        region_2_index = self.comboBoxRegion2.currentIndex()

        group_1 = self.analysis.cohort.groups[comparison.groups[0]].name
        group_2 = self.analysis.cohort.groups[comparison.groups[1]].name
        measure = comparison.sub_measure
        param = '-'
        binary_value = float_to_string_fix_decimals(comparison.binary_value)
        region = self.comboBoxRegion.currentText()
        region_2 = self.comboBoxRegion2.currentText()
        longitudinal = str(comparison.longitudinal)
        p_value_1 = comparison.p_values[0]
        p_value_2 = comparison.p_values[1]
        CI_1 = comparison.confidence_interval[0]
        CI_2 = comparison.confidence_interval[1]
        if self.measure_type == Measure.BINODAL:
            value_1 = value_1[region_1_index][region_2_index]
            value_2 = value_2[region_1_index][region_2_index]
            p_value_2 = p_value_2[region_1_index][region_2_index]
            p_value_1 = p_value_1[region_1_index][region_2_index]
            CI_1 = CI_1[region_1_index][region_2_index]
            CI_2 = CI_2[region_1_index][region_2_index]
        elif self.measure_type == Measure.NODAL:
            value_1 = value_1[region_1_index]
            value_2 = value_2[region_1_index]
            p_value_2 = p_value_2[region_1_index]
            p_value_1 = p_value_1[region_1_index]
            CI_1 = CI_1[region_1_index]
            CI_2 = CI_2[region_1_index]
        difference = float_to_string(value_2 - value_1)
        p_value_1 = float_to_string(p_value_1)
        p_value_2 = float_to_string(p_value_2)
        CI_1 = float_to_string(CI_1)
        CI_2 = float_to_string(CI_2)
        value_1 = float_to_string(value_1)
        value_2 = float_to_string(value_2)

        content = [group_1, group_2, measure, param, binary_value, region, region, region_2,
                    longitudinal, p_value_1, p_value_2, CI_1, CI_2, value_1, value_2, difference]

        mask = self.comparison_mask()
        content = np.array(content)[np.where(mask)[0]].tolist()
        return content

    def random_comparison_mask(self):
        binary = self.analysis.is_binary()
        nodal = self.measure_type == Measure.NODAL
        binodal = self.measure_type == Measure.BINODAL
        mask = [True, True, True, binary, nodal, binodal, binodal] + [True]*10
        return mask

    def random_comparison_labels(self):
        rule_binary = self.analysis.graph_settings.rule_binary
        labels = ['Group', 'Measure', 'Param', rule_binary, 'Region', 'Region 1', 'Region 2',
                  'Attempts per edge', 'Number of weights', 'Randomization number',
                  'p (1-tailed)', 'p (2-tailed)', 'CI lower', 'CI upper', 'Measure', 'Random mean', 'Difference']

        mask = self.random_comparison_mask()
        labels = np.array(labels)[np.where(mask)[0]].tolist()
        return labels

    def random_comparison_contents(self, random_comparison):
        measure_value = random_comparison.measure
        random_mean = random_comparison.mean_random_measures

        region_1_index = self.comboBoxRegion.currentIndex()
        region_2_index = self.comboBoxRegion2.currentIndex()

        group = self.analysis.cohort.groups[random_comparison.group_index].name
        measure = random_comparison.sub_measure
        param = '-'
        binary_value = float_to_string_fix_decimals(random_comparison.binary_value)
        region = self.comboBoxRegion.currentText()
        region_2 = self.comboBoxRegion2.currentText()
        attempts_per_edge = random_comparison.attempts_per_edge
        number_of_weights = random_comparison.number_of_weights
        randomization_number = random_comparison.randomization_number
        difference = random_comparison.difference
        p_value_1 = random_comparison.p_values[0]
        p_value_2 = random_comparison.p_values[1]
        CI_1 = random_comparison.confidence_intervals[0]
        CI_2 = random_comparison.confidence_intervals[1]
        if self.measure_type == Measure.BINODAL:
            difference = difference[region_1_index][region_2_index]
            measure_value = measure_value[region_1_index][region_2_index]
            random_mean = random_mean[region_1_index][region_2_index]
            p_value_2 = p_value_2[region_1_index][region_2_index]
            p_value_1 = p_value_1[region_1_index][region_2_index]
            CI_1 = CI_1[region_1_index][region_2_index]
            CI_2 = CI_2[region_1_index][region_2_index]
        elif self.measure_type == Measure.NODAL:
            difference = difference[region_1_index]
            measure_value = measure_value[region_1_index]
            random_mean = random_mean[region_1_index]
            p_value_2 = p_value_2[region_1_index]
            p_value_1 = p_value_1[region_1_index]
            CI_1 = CI_1[region_1_index]
            CI_2 = CI_2[region_1_index]
        difference = float_to_string(difference)
        p_value_1 = float_to_string(p_value_1)
        p_value_2 = float_to_string(p_value_2)
        CI_1 = float_to_string(CI_1)
        CI_2 = float_to_string(CI_2)
        measure_value = float_to_string(measure_value)
        random_mean = float_to_string(random_mean)

        content = [group, measure, param, binary_value, region, region, region_2,
                   attempts_per_edge, number_of_weights, randomization_number,
                   p_value_1, p_value_2, CI_1, CI_2, measure_value, random_mean, difference]

        mask = self.random_comparison_mask()
        content = np.array(content)[np.where(mask)[0]].tolist()
        return content

    def get_selected(self):
        return self.tableWidget.get_selected()

    def export_txt(self, file_name):
        table_string = ''
        for column in range(self.tableWidget.columnCount()):
            table_string += self.tableWidget.horizontalHeaderItem(column).text()
            table_string += ' '
        table_string += '\n'
        for row in range(self.tableWidget.rowCount()):
            for column in range(self.tableWidget.columnCount()):
                table_string += self.tableWidget.item(row, column).text()
                table_string += ' '
            table_string += '\n'
        with open(file_name, 'w') as f:
            f.write(table_string)

    def export_xlsx(self, file_name):
        table = {}
        for column in range(self.tableWidget.columnCount()):
            header = self.tableWidget.horizontalHeaderItem(column).text()
            data = []
            for row in range(self.tableWidget.rowCount()):
                data.append(self.tableWidget.item(row, column).text())
            table[header] = data
        df = pd.DataFrame.from_dict(table)
        with open(file_name, 'w') as f:
            df.to_excel(file_name, index = None, columns = None)

    def export(self, file_type, export_function):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getSaveFileName(self, "Export data",
                                                      "untitled.{}".format(file_type),
                                                      "{} files (*.{})".format(file_type, file_type),
                                                      options = options)
        if file_name:
            export_function(file_name)

