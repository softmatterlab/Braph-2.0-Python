from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative, FloatDelegate, float_to_string

ui_file = abs_path_from_relative(__file__, "../ui_files/measures_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class MeasuresWidget(Base, Form):
    def __init__(self, parent = None):
        super(MeasuresWidget, self).__init__(parent)
        self.setupUi(self)
        self.init_buttons()
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def init(self, measure_type, analysis):
        self.analysis = analysis
        self.measure_type = measure_type
        if measure_type == 'global':
            self.comboBoxRegion.hide()
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

    def init_combo_boxes(self):
        self.comboBoxRegion.currentIndexChanged.connect(self.region_changed)
        self.comboBoxGroup1.currentIndexChanged.connect(self.group_changed)
        self.comboBoxGroup2.currentIndexChanged.connect(self.group_changed)

        for group in self.analysis.cohort.groups:
            self.comboBoxGroup1.addItem(group.name)
            self.comboBoxGroup2.addItem(group.name)

        for label in self.analysis.cohort.atlas.get_brain_region_labels():
            self.comboBoxRegion.addItem(label)

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
        self.update_table()

    def comparison(self):
        self.comboBoxGroup2.setEnabled(True)
        self.update_table()

    def random_comparison(self):
        self.comboBoxGroup2.setEnabled(False)
        self.update_table()

    def region_changed(self):
        self.update_table()

    def group_changed(self):
        self.update_table()

    def update_table(self):
        if self.measure_type == 'global':
            self.update_global_table()
        elif self.measure_type == 'nodal':
            self.update_nodal_table()
        elif self.measure_type == 'binodal':
            self.update_binodal_table()

    def update_global_table(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        current_group_1 = self.comboBoxGroup1.currentIndex()
        current_group_2 = self.comboBoxGroup2.currentIndex()
        if self.btnMeasure.isChecked():
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setHorizontalHeaderLabels(['Value', 'Notes', 'Measure', 'Group', 'Param'])
            self.measurement_index_mapping = {}
            for i, measurement in enumerate(self.analysis.measurements):
                if measurement.is_global() and current_group_1 == measurement.group:
                    row = self.tableWidget.rowCount()
                    self.measurement_index_mapping[row] = i
                    self.tableWidget.setRowCount(row + 1)
                    item = QTableWidgetItem(float_to_string(measurement.value))
                    self.tableWidget.setItem(row, 0, item)
                    item = QTableWidgetItem('-')
                    self.tableWidget.setItem(row, 1, item)
                    item = QTableWidgetItem(measurement.sub_measure)
                    self.tableWidget.setItem(row, 2, item)
                    item = QTableWidgetItem(self.analysis.cohort.groups[measurement.group].name)
                    self.tableWidget.setItem(row, 3, item)
                    item = QTableWidgetItem('-')
                    self.tableWidget.setItem(row, 4, item)
        elif self.btnComparison.isChecked():
            self.tableWidget.setColumnCount(12)
            self.tableWidget.setHorizontalHeaderLabels(['Difference', 'p (1-tailed)', 'p (2-tailed)', 'Value 1', 'Value 2', 'CI lower', 'CI upper', 'Notes', 'Measure', 'Group 1', 'Group 2', 'Param'])
            self.comparison_index_mapping = {}
            for i, comparison in enumerate(self.analysis.comparisons):
                if comparison.measure_class.is_global(comparison.sub_measure) and current_group_1 == comparison.groups[0] and current_group_2 == comparison.groups[1]:
                    row = self.tableWidget.rowCount()
                    self.comparison_index_mapping[row] = i
                    self.tableWidget.setRowCount(row + 1)
                    item = QTableWidgetItem(float_to_string(comparison.measures[1] - comparison.measures[0]))
                    self.tableWidget.setItem(row, 0, item)
                    item = QTableWidgetItem(float_to_string(comparison.p_values[0]))
                    self.tableWidget.setItem(row, 1, item)
                    item = QTableWidgetItem(float_to_string(comparison.p_values[1]))
                    self.tableWidget.setItem(row, 2, item)
                    item = QTableWidgetItem(float_to_string(comparison.measures[0]))
                    self.tableWidget.setItem(row, 3, item)
                    item = QTableWidgetItem(float_to_string(comparison.measures[1]))
                    self.tableWidget.setItem(row, 4, item)
                    item = QTableWidgetItem(float_to_string(comparison.confidence_interval[0]))
                    self.tableWidget.setItem(row, 5, item)
                    item = QTableWidgetItem(float_to_string(comparison.confidence_interval[1]))
                    self.tableWidget.setItem(row, 6, item)
                    item = QTableWidgetItem('-')
                    self.tableWidget.setItem(row, 7, item)
                    item = QTableWidgetItem(comparison.sub_measure)
                    self.tableWidget.setItem(row, 8, item)
                    item = QTableWidgetItem(self.analysis.cohort.groups[comparison.groups[0]].name)
                    self.tableWidget.setItem(row, 9, item)
                    item = QTableWidgetItem(self.analysis.cohort.groups[comparison.groups[1]].name)
                    self.tableWidget.setItem(row, 10, item)
                    item = QTableWidgetItem('-')
                    self.tableWidget.setItem(row, 11, item)
        elif self.btnRandomComparison.isChecked():
            self.tableWidget.setColumnCount(10)
            self.tableWidget.setHorizontalHeaderLabels(['Comp value', 'p (1-tailed)', 'p (2-tailed)', 'Real value', 'CI lower', 'CI upper', 'Notes', 'Measure', 'Group', 'Param'])

    def update_nodal_table(self):
        pass

    def update_binodal_table(self):
        pass

    def get_selected(self):
        selected = [item.row() for item in self.tableWidget.selectionModel().selectedRows()]
        return selected

