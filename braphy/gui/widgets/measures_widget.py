from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
import pandas as pd
from braphy.utility.helper_functions import abs_path_from_relative, FloatDelegate, float_to_string
from braphy.graph.measures.measure import Measure
from braphy.workflows.MRI.subject_MRI import SubjectMRI
from braphy.workflows.fMRI.subject_fMRI import SubjectfMRI

ui_file = abs_path_from_relative(__file__, "../ui_files/measures_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class MeasuresWidget(Base, Form):
    def __init__(self, parent = None):
        super(MeasuresWidget, self).__init__(parent)
        self.setupUi(self)
        self.init_buttons()
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def init(self, measure_type, analysis):
        self.analysis = analysis
        self.measure_type = measure_type
        if measure_type == Measure.GLOBAL:
            self.comboBoxRegion.hide()
            self.comboBoxRegion2.hide()
            self.labelRegion.hide()
        elif measure_type == Measure.NODAL:
            self.comboBoxRegion2.hide()
        if analysis.cohort.subject_class == SubjectMRI:
            self.btnGroup.hide()
            self.btnSubject.hide()
            self.comboBoxSubject.hide()
        if analysis.graph_settings.weighted:
            self.binaryPlotWidget.hide()
        self.init_combo_boxes()
        self.btnMeasure.setChecked(True)
        self.measure()

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

        self.btnExportTxt.clicked.connect(lambda state, file_type = 'txt', export_function = self.export_txt: self.export(file_type, export_function))
        self.btnExportXlsx.clicked.connect(lambda state, file_type = 'xlsx', export_function = self.export_xlsx: self.export(file_type, export_function))

    def init_combo_boxes(self):
        self.comboBoxRegion.currentIndexChanged.connect(self.update_table)
        self.comboBoxRegion2.currentIndexChanged.connect(self.update_table)
        self.comboBoxGroup1.currentIndexChanged.connect(self.update_table)
        self.comboBoxGroup2.currentIndexChanged.connect(self.update_table)
        self.comboBoxSubject.currentIndexChanged.connect(self.update_table)

        for group in self.analysis.cohort.groups:
            self.comboBoxGroup1.addItem(group.name)
            self.comboBoxGroup2.addItem(group.name)

        for label in self.analysis.cohort.atlas.get_brain_region_labels():
            self.comboBoxRegion.addItem(label)
            self.comboBoxRegion2.addItem(label)

    def remove(self):
        selected = self.get_selected()
        for i in range(len(selected) - 1, -1, -1):
            if self.btnMeasure.isChecked():
                index_to_remove = self.measurement_index_mapping[selected[i]]
                del self.analysis.measurements[index_to_remove]
            elif self.btnComparison.isChecked():
                index_to_remove = self.comparison_index_mapping[selected[i]]
                del self.analysis.comparisons[index_to_remove]
            elif self.btnRandomComparison.isChecked():
                index_to_remove = self.random_comparison_index_mapping[selected[i]]
                del self.analysis.random_comparisons[index_to_remove]
        self.update_table()

    def measure(self):
        self.comboBoxGroup2.setEnabled(False)
        self.comboBoxSubject.setEnabled(True)
        self.btnSubject.setEnabled(True)
        self.labelGroup.setText('Choose group:')
        self.update_table()

    def comparison(self):
        self.comboBoxGroup2.setEnabled(True)
        self.comboBoxSubject.setEnabled(False)
        self.btnSubject.setEnabled(False)
        self.labelGroup.setText('Choose groups:')
        self.btnGroup.blockSignals(True)
        self.btnGroup.setChecked(True)
        self.btnGroup.blockSignals(False)
        self.update_table()

    def random_comparison(self):
        self.comboBoxGroup2.setEnabled(False)
        self.comboBoxSubject.setEnabled(True)
        self.btnSubject.setEnabled(True)
        self.labelGroup.setText('Choose group:')
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
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        current_group_1 = self.comboBoxGroup1.currentIndex()
        current_group_2 = self.comboBoxGroup2.currentIndex()
        current_region_index = self.comboBoxRegion.currentIndex()
        if self.btnMeasure.isChecked():
            self.update_measurements_table(current_group_1, current_region_index)
        elif self.btnComparison.isChecked():
            self.update_comparison_table(current_group_1, current_group_2, current_region_index)
        elif self.btnRandomComparison.isChecked():
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
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setHorizontalHeaderLabels(['Comp value', 'p (1-tailed)', 'p (2-tailed)', 'Real value', 'CI lower', 'CI upper', 'Notes', 'Measure', 'Group', 'Param'])

    def measurement_mask(self):
        subject = self.analysis.cohort.subject_class == SubjectfMRI and not self.btnGroup.isChecked()
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
        if self.analysis.cohort.subject_class == SubjectfMRI:
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
        binary_value = measurement.binary_value
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
        subject = self.analysis.cohort.subject_class == SubjectfMRI and not self.btnGroup.isChecked()
        binary = self.analysis.is_binary()
        nodal = self.measure_type == Measure.NODAL
        binodal = self.measure_type == Measure.BINODAL
        mask = [True, True, subject, True, True, binary, nodal, binodal, binodal] + [True]*8

        return mask

    def comparison_labels(self):
        rule_binary = self.analysis.graph_settings.rule_binary
        labels = ['Group 1', 'Group 2', 'Subject', 'Measure', 'Param', rule_binary, 'Region', 'Region 1', 'Region 2',
                  'Longitudinal', 'p (1-tailed)', 'p (2-tailed)', 'CI lower', 'CI upper', 'Value 1', 'Value 2', 'Difference']

        mask = self.comparison_mask()
        labels = np.array(labels)[np.where(mask)[0]].tolist()
        return labels

    def comparison_contents(self, comparison):
        if self.analysis.cohort.subject_class == SubjectfMRI:
            value_1 = np.mean(comparison.measures[0], axis = 0)
            value_2 = np.mean(comparison.measures[1], axis = 0)
        else:
            value_1 = comparison.measures[0]
            value_2 = comparison.measures[1]

        region_1_index = self.comboBoxRegion.currentIndex()
        region_2_index = self.comboBoxRegion2.currentIndex()

        group_1 = self.analysis.cohort.groups[comparison.groups[0]].name
        group_2 = self.analysis.cohort.groups[comparison.groups[1]].name
        subject = self.comboBoxSubject.currentText()
        measure = comparison.sub_measure
        param = '-'
        binary_value = comparison.binary_value
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
        elif self.measure_type == Measure.NODAL:
            value_1 = value_1[region_1_index]
            value_2 = value_2[region_1_index]
            p_value_2 = p_value_2[region_1_index]
            p_value_1 = p_value_1[region_1_index]
        difference = float_to_string(value_2 - value_1)
        p_value_1 = float_to_string(p_value_1)
        p_value_2 = float_to_string(p_value_2)
        CI_1 = float_to_string(CI_1)
        CI_2 = float_to_string(CI_2)
        value_1 = float_to_string(value_1)
        value_2 = float_to_string(value_2)

        content = [group_1, group_2, subject, measure, param, binary_value, region, region, region_2,
                    longitudinal, p_value_1, p_value_2, CI_1, CI_2, value_1, value_2, difference]

        mask = self.comparison_mask()
        content = np.array(content)[np.where(mask)[0]].tolist()
        return content

    def get_selected(self):
        selected = [item.row() for item in self.tableWidget.selectionModel().selectedRows()]
        return selected

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

